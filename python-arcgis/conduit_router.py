# conduit_router.py
# Part of the EzeeFiber OSP Design Toolbox (ArcGIS Pro Python Toolbox)
# Automates conduit route creation from cabinet locations to service addresses.

import arcpy
import os
from typing import Optional


class ConduitRouter(object):
    """ArcGIS Pro Python Toolbox tool for automated conduit routing.

    Routes conduit from a selected cabinet feature to all service
    address points within a user-defined buffer distance.

    Inputs:
        - Cabinet layer (point feature class)
        - Address point layer (point feature class)
        - Road centerline network dataset
        - Buffer distance (feet)
        - Conduit type (innerduct count, diameter)

    Outputs:
        - Conduit route polyline features with auto-populated attributes
    """

    def __init__(self):
        self.label = 'Conduit Router'
        self.description = 'Route conduit from cabinet to address points along road network.'
        self.canRunInBackground = False

    def getParameterInfo(self):
        params = []

        cabinet_lyr = arcpy.Parameter(
            displayName='Cabinet Layer',
            name='cabinet_lyr',
            datatype='GPFeatureLayer',
            parameterType='Required',
            direction='Input'
        )
        cabinet_lyr.filter.list = ['Point']
        params.append(cabinet_lyr)

        address_lyr = arcpy.Parameter(
            displayName='Address Point Layer',
            name='address_lyr',
            datatype='GPFeatureLayer',
            parameterType='Required',
            direction='Input'
        )
        address_lyr.filter.list = ['Point']
        params.append(address_lyr)

        network_ds = arcpy.Parameter(
            displayName='Road Network Dataset',
            name='network_ds',
            datatype='DENetworkDataset',
            parameterType='Required',
            direction='Input'
        )
        params.append(network_ds)

        buffer_dist = arcpy.Parameter(
            displayName='Service Buffer Distance (feet)',
            name='buffer_dist',
            datatype='GPDouble',
            parameterType='Required',
            direction='Input'
        )
        buffer_dist.value = 500.0
        params.append(buffer_dist)

        conduit_type = arcpy.Parameter(
            displayName='Conduit Type',
            name='conduit_type',
            datatype='GPString',
            parameterType='Required',
            direction='Input'
        )
        conduit_type.filter.type = 'ValueList'
        conduit_type.filter.list = ['1.25in-1ct', '1.25in-2ct', '2in-1ct', '2in-4ct']
        conduit_type.value = '1.25in-2ct'
        params.append(conduit_type)

        output_fc = arcpy.Parameter(
            displayName='Output Conduit Routes',
            name='output_fc',
            datatype='DEFeatureClass',
            parameterType='Required',
            direction='Output'
        )
        params.append(output_fc)

        return params

    def isLicensed(self):
        try:
            return arcpy.CheckExtension('Network') == 'Available'
        except Exception:
            return False

    def execute(self, parameters, messages):
        cabinet_lyr = parameters[0].valueAsText
        address_lyr = parameters[1].valueAsText
        network_ds = parameters[2].valueAsText
        buffer_dist = parameters[3].value
        conduit_type = parameters[4].valueAsText
        output_fc = parameters[5].valueAsText

        scratch = arcpy.env.scratchGDB
        arcpy.env.overwriteOutput = True

        messages.addMessage('Step 1: Buffering cabinet locations...')
        cabinet_buffer = os.path.join(scratch, 'cabinet_buffer')
        arcpy.analysis.Buffer(
            in_features=cabinet_lyr,
            out_feature_class=cabinet_buffer,
            buffer_distance_or_field=f'{buffer_dist} Feet',
            line_side='FULL',
            dissolve_option='NONE'
        )

        messages.addMessage('Step 2: Selecting addresses within buffer...')
        arcpy.management.MakeFeatureLayer(address_lyr, 'addr_temp')
        arcpy.management.SelectLayerByLocation(
            in_layer='addr_temp',
            overlap_type='WITHIN',
            select_features=cabinet_buffer
        )

        addr_count = int(arcpy.management.GetCount('addr_temp').getOutput(0))
        messages.addMessage(f'Found {addr_count} addresses within buffer.')

        if addr_count == 0:
            messages.addWarning('No addresses found within buffer distance. Adjust buffer and retry.')
            return

        messages.addMessage('Step 3: Solving closest facility network routes...')
        nd_layer = 'nd_layer'
        arcpy.nax.MakeNetworkDatasetLayer(network_ds, nd_layer)
        
        cf = arcpy.nax.ClosestFacility(nd_layer)
        cf.defaultTargetFacilityCount = 1
        cf.travelMode = arcpy.nax.GetTravelModes(nd_layer)['Driving Distance']
        cf.distanceUnits = arcpy.nax.DistanceUnits.Feet

        cf.load(arcpy.nax.ClosestFacilityInputDataType.Facilities, cabinet_lyr)
        cf.load(arcpy.nax.ClosestFacilityInputDataType.Incidents, 'addr_temp')

        result = cf.solve()

        if not result.solveSucceeded:
            messages.addError('Network solve failed. Check network dataset and inputs.')
            return

        messages.addMessage('Step 4: Exporting routes and populating attributes...')
        result.export(arcpy.nax.ClosestFacilityOutputDataType.Routes, output_fc)

        ConduitRouter._add_conduit_attributes(output_fc, conduit_type, messages)

        messages.addMessage(f'Done. Conduit routes written to: {output_fc}')

    @staticmethod
    def _add_conduit_attributes(
        feature_class: str,
        conduit_type: str,
        messages,
    ) -> None:
        """Add and populate standard conduit attribute fields."""
        fields_to_add = [
            ('CONDUIT_TYPE', 'TEXT', 20),
            ('INNERDUCT_CT', 'SHORT', None),
            ('DIAMETER_IN', 'FLOAT', None),
            ('INSTALL_DEPTH', 'SHORT', None),
            ('BORE_REQUIRED', 'TEXT', 5),
        ]

        for fname, ftype, flength in fields_to_add:
            kwargs = {'field_length': flength} if flength else {}
            arcpy.management.AddField(feature_class, fname, ftype, **kwargs)

        size, count_str = conduit_type.split('-')
        diameter = float(size.replace('in', ''))
        innerduct_count = int(count_str.replace('ct', ''))

        with arcpy.da.UpdateCursor(
            feature_class,
            ['CONDUIT_TYPE', 'INNERDUCT_CT', 'DIAMETER_IN', 'INSTALL_DEPTH', 'BORE_REQUIRED']
        ) as cursor:
            for row in cursor:
                row[0] = conduit_type
                row[1] = innerduct_count
                row[2] = diameter
                row[3] = 36  # standard burial depth in inches
                row[4] = 'NO'
                cursor.updateRow(row)

        messages.addMessage(f'Attributes populated for conduit type: {conduit_type}')

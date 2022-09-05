#!/usr/bin/python3
# -*- coding: utf-8 -*-
import boto3
import xlsxwriter
import datetime
from botocore.exceptions import ClientError

# Time 0 days ago. I mean NOW.
today = datetime.datetime.now()

"""
  Function: infoEC2VolumesReportUsage()
  Input:
    AWS_PROFILE=sso-nvsit-pu python3 infoEC2VolumesReportUsage.py
  Output:
    Excel in S3 with all report.
  Descr: Obtain a Excel file that contains info about available Volumes to be deleted.
"""

def create_excel(excelFileName):
    # Name of file XLSX Excel that contains all info.
    print("Excel File going to be created --> "+ excelFileName)

    # Create workbook.
    workbook = xlsxwriter.Workbook(f'{excelFileName}')

    # Add MAIN worksheet to the workbook.
    main_worksheet = workbook.add_worksheet('INFORMATION')

    # Set auto filter on for the cells
    main_worksheet.autofilter('C3:I4')

    # Hide unused rows.
    main_worksheet.set_default_row(hide_unused_rows=True)

    # Define wihite backgroup format.
    whiteBackGroundFromat = workbook.add_format(
        {
            'bg_color': "#FFFFFF",
            'align': 'center',
            'valign': 'center',
            'font_name': 'calibri',
            'font_size': 11,
            'text_wrap': True,
            'locked': True,
            'border': 0
        }
    )

    # Merge Format for KP worksheet.
    mergedFormat = workbook.add_format(
        {
            'bg_color': "#000000",
            'font_color': "#FFFFFF",
            'align': 'center',
            'valign': 'center',
            'font_name': 'Segoe UI',
            'font_size': 15,
            'bold': 'True',
            'locked': 'True',
            'border': 0
        }
    )
    # Cells under Merged form.
    subMergedFormat = workbook.add_format(
        {
            'bg_color': "03C0FF",
            'font_color': "#FFFFFF",
            'align': 'vcenter',
            'valign': 'center',
            'font_name': 'Calibri',
            'font_size': 13,
            'bold': 'True',
            'locked': 'True',
            'border': 5,
            'top': 5,
            'bottom': 5,
            'left': 5,
            'right': 5,	
            'border_color': "#FFFFFF"
        }
    )

    grayFormatDark = workbook.add_format(
        {
            'bg_color': "#CDD1DE",
            'font_color': "#000000",
            'align': 'center',
            'valign': 'center',
            'text_wrap': True,
            'font_name': 'Calibri',
            'font_size': 10,
            'locked': 'True',
            'border': 4,
            'top': 4,
            'bottom': 4,
            'left': 4,
            'right': 4,	
            'border_color': "#FFFFFF"
        }
    )

    grayFormatDarkNum = workbook.add_format(
        {
            'bg_color': "#CDD1DE",
            'font_color': "#000000",
            'align': 'center',
            'valign': 'center',
            'text_wrap': True,
            'font_name': 'Calibri',
            'font_size': 10,
            'locked': 'True',
            'border': 4,
            'top': 4,
            'bottom': 4,
            'left': 4,
            'right': 4,	
            'border_color': "#FFFFFF",
            'num_format': 'dd.mm.yyyy'
        }
    )

    grayFormatLight = workbook.add_format(
        {
            'bg_color': "#E8E9EF",
            'font_color': "#000000",
            'align': 'center',
            'valign': 'center',
            'text_wrap': True,
            'font_name': 'Calibri',
            'font_size': 10,
            'locked': 'True',
            'border': 4,
            'top': 4,
            'bottom': 4,
            'left': 4,
            'right': 4,	
            'border_color': "#FFFFFF"
        }
    )

    grayFormatLightNum = workbook.add_format(
        {
            'bg_color': "#E8E9EF",
            'font_color': "#000000",
            'align': 'center',
            'valign': 'center',
            'text_wrap': True,
            'font_name': 'Calibri',
            'font_size': 10,
            'locked': 'True',
            'border': 4,
            'top': 4,
            'bottom': 4,
            'left': 4,
            'right': 4,	
            'border_color': "#FFFFFF",
            'num_format': 'dd.mm.yyyy'
        }
    )


    # Make the sheet white with no boarder.
    for whiteBackGroundCells in range(100): # integer odd-even alternation.
        main_worksheet.set_row(whiteBackGroundCells, cell_format=(whiteBackGroundFromat))

    # Set column width across the worksheet.
    main_worksheet.set_column("B:I", 21.57)

    # First all SSP merge cells.
    main_worksheet.merge_range('C2:I2', 'AWS', mergedFormat)

    # All headers and name of platform.
    main_worksheet.merge_range('B2:B4', 'VOLUME ID', subMergedFormat)
    main_worksheet.merge_range('C3:C4', 'REGION', subMergedFormat)
    main_worksheet.merge_range('D3:D4', 'ENCRYPTED', subMergedFormat)
    main_worksheet.merge_range('E3:E4', 'SIZE', subMergedFormat)
    main_worksheet.merge_range('F3:F4', 'VOLUMETYPE', subMergedFormat)
    main_worksheet.merge_range('G3:G4', 'SNAPSHOT', subMergedFormat)
    main_worksheet.merge_range('H3:H4', 'AVAILABILITYZONE', subMergedFormat)
    main_worksheet.merge_range('I3:I4', 'MULTIATTACHENABLED', subMergedFormat)

    # Create a tupla to use later.
    return_tupla_to_later_reuse_temporal = workbook, grayFormatDark, grayFormatDarkNum, grayFormatLight, grayFormatLightNum

    # Return tupla
    return return_tupla_to_later_reuse_temporal



def write_in_excel_Worksheet(workbook, grayFormatDark, grayFormatDarkNum, grayFormatLight, grayFormatLightNum, data_information_complete):
    # We are going to LOAD previous Worksheet.
    existingWorksheet = workbook.get_worksheet_by_name('INFORMATION')

    row = 4
    col = 1

    # Loop to print to all rows and columns.
    for VolumeId, Region, Encrypted, Size, VolumeType, Snapshot, AvailabilityZone, MultiAttachEnabled in data_information_complete:

        # Condition to format alternate rows
        if row%2 == 1:
            cellFormatFix = grayFormatDark
            cellFormatNumFix = grayFormatDarkNum
        else:
            cellFormatFix = grayFormatLight
            cellFormatNumFix = grayFormatLightNum
        existingWorksheet.write_string(row, col, VolumeId, cellFormatFix )
        existingWorksheet.write_string(row, col + 1 , Region, cellFormatFix )
        existingWorksheet.write_string(row, col + 2 , Encrypted, cellFormatFix )
        existingWorksheet.write_string(row, col + 3 , Size, cellFormatFix )
        existingWorksheet.write_string(row, col + 4 , VolumeType, cellFormatFix )
        existingWorksheet.write_string(row, col + 5 , Snapshot, cellFormatFix )
        existingWorksheet.write_string(row, col + 6 , AvailabilityZone, cellFormatFix )
        existingWorksheet.write_string(row, col + 7 , MultiAttachEnabled, cellFormatFix )
        row += 1

    workbook.close()
    print("Workbook closed")


def obtain_all_results():
    # Inicial configuration EC2.
    client = boto3.client('ec2')

    global volume_list
    volume_list = []

    # Check all regions.
    for region in client.describe_regions()['Regions']:

        # Save the region to get later all volumes.
        regions_to_check=region['RegionName']

        # Initiate boto3 in each region.
        client = boto3.client('ec2', region_name=regions_to_check)
        # Describe volumes that are in an available state.
        volumes = client.describe_volumes( Filters=[{'Name': 'status', 'Values': ['available']}])

        if volumes['Volumes']:
            # If there are volumes in an available state show print region.
            print ("\nRegion: " + regions_to_check)
        else:
            # If there are no volumes in an available state show region.
            print ("\nRegion: "+ regions_to_check + "\tNo volumes in available state")
        
        #Loop through volumes only in an available state.
        for volume in volumes['Volumes']:

            #Add volume and its region to volume_list.
            lsst = (f"{volume['VolumeId']}|{regions_to_check}|{volume['Encrypted']}|{volume['Size']}|{volume['VolumeType']}|{volume['SnapshotId']}|{volume['AvailabilityZone']}|{volume['MultiAttachEnabled']}")
            volume_list.append(lsst.split('|'))

            # Information ID of every volume.
            print ("Volume:  " + volume['VolumeId'])

    if volume_list:
        # Get the list of volumes in state available.
        print ("\nYou have "+str(len(volume_list)) +" volumes in an available state")
        return volume_list
    else:
        #Exit if not volumes.
        print("\nYou have no volumes in an available state")
        print("\nExiting")
        exit()


##########################################
######  infoEC2VolumesReportUsage.py #####
##########################################

# Excel Name.
excelFileName = ('infoEC2VolumesReportUsage' +  '-' + today.strftime("%d""-""%b") + '.xlsx')

# First execution
try:
    data_information_complete = obtain_all_results()
    # Create Excel and return tupla with all neccesary to later write with data.
    return_tupla_to_later_reuse = create_excel(excelFileName)
    # Write in an excel.
    write_in_excel_Worksheet(return_tupla_to_later_reuse[0], return_tupla_to_later_reuse[1], return_tupla_to_later_reuse[2], return_tupla_to_later_reuse[3], return_tupla_to_later_reuse[4], data_information_complete)
except:
    ClientError

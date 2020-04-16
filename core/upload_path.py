import os
import xlsxwriter

import io
from urllib.request import urlopen

def get_images_upload_path(instance, filename):
    return os.path.join(
        'profile',
        instance.__class__.__name__.lower(),
        str(instance.id),
        filename
    )

def get_events_upload_path(instance, filename):
    return os.path.join(
        'images',
        instance.__class__.__name__.lower(),
        str(instance.id),
        filename
    )

def get_images_path(instance, filename):
    return os.path.join('images', 'houses', filename)

def handle_uploaded_file(instance, filename):
    return os.path.join(
        'pdf',
        instance.__class__.__name__.lower(),
        str(instance.id),
        filename
    )

def generate_soa_report(payload):
    os_path = "media/excell/"
    try:
        os_path_directory = os.mkdir(os_path)
    except OSError:
        print ('Directory is already created')

    workbook = xlsxwriter.Workbook(os_path + 'generate_soa_report.xlsx')
    # https://xlsxwriter.readthedocs.io/workbook.html > workbook.add_worksheet()
    worksheet = workbook.add_worksheet()
    # https://xlsxwriter.readthedocs.io/example_protection.html # NOTE: no one can edit
    worksheet.protect()
    cell_format = workbook.add_format()

    # https://xlsxwriter.readthedocs.io/format.html#set_align
    cell_format.set_align('right')
    cell_format.set_align('vcenter')

    worksheet.write('K1', 'Aeon Luxe Properties, Inc.', workbook.add_format({'bold': True, 'align': 'right', 'valign': 'vcenter'}))
    worksheet.write('K2', 'Mezzanine, FTC Tower,', cell_format)
    worksheet.write('K3', '1034 Mt. Apo St.', cell_format)
    worksheet.write('K4', 'Davao City 8000', cell_format)
    worksheet.write('K5', '(+63 82) 305-0588', cell_format)
    worksheet.write('K6', 'marketing@aeonluxe.com.ph', cell_format)

    worksheet.set_column('A:J', 18)
    worksheet.set_column('K:K', 25)

    # https://xlsxwriter.readthedocs.io/example_merge1.html
    merge_format = workbook.add_format({
        'bold': 2,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': '#FBB730'})

    worksheet.merge_range('A8:K9', 'Statement Of Account', merge_format)

    data = [
        ['Unit Number', 'Description', 'Invoice No', 'Invoice Date', 'Total Dues', 'After Total Dues', 'Current Penalty', 'Owned By', 'First name', 'Previous Balance', 'Recurring Monthly Dues']
    ]
    vals = []
    for x in payload.values_list('unit__number', 'description', 'invoice_no', 'invoice_date', 'total_dues', 'after_total_dues', 'current_penalty', 'owned_by', 'user__first_name', 'previous_balance', 'recurring_monthly_dues'):
        vals.append(list(x))

    for index, y in enumerate(vals, start=0):
        vals[index][3] = vals[index][3].strftime("%B %d, %Y")
        data.append(vals[index])

    # https://xlsxwriter.readthedocs.io/worksheet.html > worksheet.insert_image()
    url = 'https://i.imgur.com/qtGb6wH.png'
    image_data = io.BytesIO(urlopen(url).read())

    worksheet.insert_image('A1', url, {'image_data': image_data, 'x_scale': 0.45, 'y_scale': 0.45})
    worksheet.add_table('A11:K' + str((len(data) + 11)), {'data': data, 'header_row': False, 'style': None})
    workbook.close()


def generate_excell_from_filter(payload, additional):
    # https://xlsxwriter.readthedocs.io/example_images.html

    workbook = xlsxwriter.Workbook('media/excell/generate_excell.xlsx')
    # https://xlsxwriter.readthedocs.io/workbook.html > workbook.add_worksheet()
    worksheet = workbook.add_worksheet()
    worksheet1 = workbook.add_worksheet('graph')
    chart = workbook.add_chart({'type': 'column'})
    chart1 = workbook.add_chart({'type': 'column'})

    data = [
        ['id', 'Message', 'Status', 'Image', 'First Name', 'Last Name', 'Creation Date', 'IMAGE']
    ]
    vals = []
    graph = []
    inc = 1
    for x in payload.values_list('id', 'message', 'status', 'user__profile__image', 'user__first_name', 'user__last_name', 'creation_date__date'):
        vals.append(list(x))

    for index, y in enumerate(vals, start=0):
        vals[index][6] = vals[index][6].strftime("%B %d, %Y")
        inc = inc + 1
        if (vals[index][3] != None):
            image = vals[index][3].replace('profile', 'media/profile')
            worksheet.insert_image('H'+str(int(inc)), image, {'x_scale': 0.05, 'y_scale': 0.05})
        data.append(vals[index])

    # for grpahs
    graph.append(additional['feedbackdates'])

    chart.add_series({
        'values': '=Sheet1!$A$1:$A$12',
        'line':   {'color': '#FF9900'},
    })
    chart.set_title({
        'name': 'Reports This Year (2020)',
        'name_font': {
            'name': 'Calibri',
            'color': 'blue',
        },
    })
    chart.set_x_axis({
        'name': 'Month',
        'name_font': {
            'name': 'Courier New',
            'color': '#92D050'
        },
        'num_font': {
            'name': 'Arial',
            'color': '#00B0F0',
        },
    })
    chart1.add_series({
        'values': '=Sheet1!$A$1:$A$12',
        'line':   {'color': '#FF9900'},
    })
    chart1.set_title({
        'name': 'Reports This Year (2020)',
        'name_font': {
            'name': 'Calibri',
            'color': 'blue',
        },
    })
    chart1.set_x_axis({
        'name': 'Month',
        'name_font': {
            'name': 'Courier New',
            'color': '#92D050'
        },
        'num_font': {
            'name': 'Arial',
            'color': '#00B0F0',
        },
    })
    worksheet1.insert_chart('A2', chart)
    worksheet1.insert_chart('J2', chart1)
    worksheet.add_table('A1:H' + str(len(data)), {'data': data, 'header_row': False})

    workbook.close()

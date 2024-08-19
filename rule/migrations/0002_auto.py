from django.db import migrations


def insert_initial_data(apps, schema_editor):
    Rule = apps.get_model('rule', 'Rule')
    initial_data = [
        {
            "name": "WeekendScheduling",
            "value": {
                "Friday": 1,
                "Saturday": 4,
                "Sunday": 3
            }
        },
        {
            "name": "LeagueStartDate",
            "value": "2024-01-05"
        },
        {
          "name": "KickOff",  # New rule
          "value": ["14:00", "15:30", "18:00"] # Example kick-off time (2:00 PM)
        },
        {
            "name": "FIFACALENDAR",  # New rule
            "value": [
                {
                    "month": "September",
                    "start_date": "2024-09-2",
                    "end_date": "2024-09-10"
                },
                {
                    "month": "October",
                    "start_date": "2024-10-07",
                    "end_date": "2024-10-15"
                },
                {
                    "month": "November",
                    "start_date": "2024-11-11",
                    "end_date": "2024-11-19"
                },
                {
                    "month": "December",
                    "start_date": "0000-00-00",
                    "end_date": "0000-00-00"
                },
                {
                    "month": "January",
                    "start_date": "0000-00-00",
                    "end_date": "0000-00-00"
                },
                {
                    "month": "February",
                    "start_date": "0000-00-00",
                    "end_date": "0000-00-00"
                },
                {
                    "month": "March",
                    "start_date": "2025-03-17",
                    "end_date": "2025-03-25"
                },
                {
                    "month": "April",
                    "start_date": "0000-00-00",
                    "end_date": "0000-00-00"
                },
                {
                    "month": "May",
                    "start_date": "0000-00-00",
                    "end_date": "0000-00-00"
                },
                {
                    "month": "June",
                    "start_date": "0000-00-00",
                    "end_date": "0000-00-00"
                },
                {
                    "month": "July",
                    "start_date": "0000-00-00",
                    "end_date": "0000-00-00"
                },
            ]
        }
    ]
    for data in initial_data:
        Rule.objects.create(name=data['name'], value=data['value'])



class Migration(migrations.Migration):

    dependencies = [
        ('rule', '0001_initial'),  # Add the appropriate previous migration number
    ]

    operations = [
        migrations.RunPython(insert_initial_data),
    ]

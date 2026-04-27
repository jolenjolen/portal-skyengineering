"""
Author: Muhammed Hasan
Descroption: Noticed users had null value for team so had to populate team column form excel.
"""

import os
import django
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portal.settings")
django.setup()

from core.models import TblUser, TblTeam

Excel_File = "team_registry.xlsx"

def assign_team_to_user():
    data = pd.read_excel(Excel_File)

    updated = 0
    missing_user = 0
    missing_team = 0

    for index,row in data.iterrows():
        team_leader = str(row["Team Leader"]).strip()
        team_name = str(row["Team Name"]).strip()

        names = team_leader.split(" ",1)

        if len(names)<2:
            print(f"Skipped invalid name: {team_leader}")
            continue
        first_name = names[0]
        surname = names[1]

        user = TblUser.objects.filter(
            fname__iexact=first_name,
            sname__iexact=surname,
            ).first()

        team = TblTeam.objects.filter(name__iexact=team_name).first()

        if not user:
            missing_user +=1
            print(f"User not found: {team_leader}")
            continue

        if not team: 
            missing_team+=1
            print(f"Team not found: {team_name}")
            continue

        user.team = team
        user.save(update_fields=["team"])

        updated =+1
        print(f"Assigned {user.fname} {user.sname} to {team.name}")

    print("Finished assigning user teams.")
    print(f"Users updated: {updated}")
    print(f"Missing users: {missing_user}")
    print(f"Missing teams: {missing_team}")

assign_team_to_user()

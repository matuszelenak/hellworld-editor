from django.contrib.auth.hashers import make_password
from django.db import migrations

from people.models import Team, Participant


def create_teams_participants(apps, schema_editor):
    teams = [
        Team.objects.create(
            name=f'Team {team_id + 1}'
        )
        for team_id in range(6)
    ]

    participants = [
        ('AdamZahradnik', 'RoyaltyRayWhySkin', 2),
        ('AdrianKabac', 'DescendSelfishLateFreeze', -1),
        ('AdriankaJanackova', 'DisapproveScrapeSearchGood', -1),
        ('BohdanJoza', 'SaddleCageAppointRain', 5),
        ('DanielMedveď', 'OnBowOutwardFill', -1),
        ('DanielOravec', 'TellChickenCardFlour', -1),
        ('DanielTimko', 'CheeseHoweverUntilSuspect', -1),
        ('DavidMisiak', 'DuckWelcomeHumanCircle', -1),
        ('EduardRuisl', 'PullTaxiRollEverything', 3),
        ('ElaVojtkova', 'InventorTapWakeWorse', -1),
        ('Gabrielasavelova', 'SpreadAbroadComparisonWhen', 2),
        ('JakubParada', 'UglySomehowPalePreserve', 2),
        ('JanGottweis', 'HideFormNewsMachinery', 3),
        ('JanPriner', 'ThinPartStrawClassify', 4),
        ('JaroslavPaska', 'MarchAbsentEastNight', 1),
        ('JiriKalvoda', 'AuntAttendTermMotherly', 3),
        ('JitkaMuravska', 'SettleStrapKneeAmuse', 3),
        ('Jozefciz', 'LightAdventureThereforeFinger', -1),
        ('LukasJankola', 'LipstickFlattenNorMonth', 0),
        ('MarcelPalaj', 'JustPaperIllNail', 1),
        ('MarosStudenic', 'RespectExcellenceEverywhereValley', 2),
        ('MartinKoutensky', 'PassagePlentyRescueTrap', -1),
        ('MatejHanus', 'MiseryToothClimbCover', -1),
        ('MatejKliment', 'AppearanceEggSuckStage', -1),
        ('MatejStraka', 'ClassMonthExtremeStiff', -1),
        ('MatejUrban', 'ViolentUntilExpressionAnger', -1),
        ('MichalFarnbauer', 'BucketEntranceSweetFormal', 4),
        ('MichalKodad', 'DineAnyPumpInstead', -1),
        ('MichalStanik', 'ChooseTidyLeatherSpeech', 0),
        ('PavolKycina', 'ThoroughMilkFarServe', 1),
        ('SabinaSamporova', 'ExtensiveBranchPageSoft', 1),
        ('Samuelcavoj', 'ThenPourBriberyProper', 5),
        ('SamuelKrajci', 'BehindNounDotAshamed', 0),
        ('stefanSlavkovsky', 'MotherlyThunderDirtEnvy', 5),
        ('MinhDangHuy', 'SilverMysteryFutureEvil', -1),
        ('MartinKalab', 'ProposalSizeCharacterSpite', 5),
    ]
    Participant.objects.bulk_create([
        Participant(
            username=name,
            password=make_password(passwd),
            is_active=True,
            team=teams[team] if team != -1 else None
        ) for name, passwd, team in participants
    ])

    for name, passwd, _ in participants:
        print(name, passwd)


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0006_auto_20190406_1831'),
    ]

    operations = [
        migrations.RunPython(create_teams_participants)
    ]

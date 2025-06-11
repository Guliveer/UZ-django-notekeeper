from django.db import migrations

def add_school_subjects(apps, schema_editor):
    Category = apps.get_model('notes', 'Category')
    
    subjects = [
        ('matematyka', 'Matematyka', 'Przedmiot ścisły obejmujący algebrę, geometrię i analizę matematyczną'),
        ('jezyk-polski', 'Język Polski', 'Przedmiot humanistyczny obejmujący literaturę i gramatykę'),
        ('fizyka', 'Fizyka', 'Przedmiot ścisły badający prawa przyrody'),
        ('chemia', 'Chemia', 'Przedmiot ścisły badający właściwości substancji'),
        ('biologia', 'Biologia', 'Przedmiot przyrodniczy badający życie i organizmy żywe'),
        ('historia', 'Historia', 'Przedmiot humanistyczny badający przeszłość'),
        ('geografia', 'Geografia', 'Przedmiot przyrodniczy badający Ziemię i jej środowisko'),
        ('angielski', 'Język Angielski', 'Język obcy nowożytny'),
        ('niemiecki', 'Język Niemiecki', 'Język obcy nowożytny'),
        ('informatyka', 'Informatyka', 'Przedmiot techniczny obejmujący programowanie i technologie informacyjne'),
        ('wos', 'Wiedza o Społeczeństwie', 'Przedmiot humanistyczny badający społeczeństwo i politykę'),
        ('religia', 'Religia', 'Przedmiot etyczno-religijny'),
        ('wychowanie-fizyczne', 'Wychowanie Fizyczne', 'Przedmiot sportowy'),
        ('plastyka', 'Plastyka', 'Przedmiot artystyczny'),
        ('muzyka', 'Muzyka', 'Przedmiot artystyczny'),
    ]
    
    for slug, name, description in subjects:
        Category.objects.get_or_create(
            slug=slug,
            defaults={
                'name': name,
                'description': description
            }
        )

def remove_school_subjects(apps, schema_editor):
    Category = apps.get_model('notes', 'Category')
    Category.objects.filter(slug__in=[s[0] for s in subjects]).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('notes', '0005_category_comment_delete_blog_note_image_note_likes_and_more'),
    ]

    operations = [
        migrations.RunPython(add_school_subjects, remove_school_subjects),
    ] 
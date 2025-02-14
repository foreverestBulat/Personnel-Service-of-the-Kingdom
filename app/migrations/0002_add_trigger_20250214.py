from django.db import migrations

def create_trigger(apps, schema_editor):
    sql_create_trigger = """
    CREATE OR REPLACE FUNCTION check_subject_limit()
    RETURNS TRIGGER AS $$
    BEGIN
        IF (SELECT COUNT(*) FROM app_subject WHERE king_id = NEW.king_id) > 3 THEN
            RAISE EXCEPTION 'У короля уже есть 3 подданных!';
        END IF;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    CREATE TRIGGER app_subject_limit_trigger
    AFTER INSERT OR UPDATE OR DELETE ON app_subject
    FOR EACH ROW
    EXECUTE FUNCTION check_subject_limit();
    """
    
    schema_editor.execute(sql_create_trigger)

def remove_trigger(apps, schema_editor):
    sql_drop_trigger = """
    DROP TRIGGER IF EXISTS app_subject_limit_trigger ON app_subject;
    """
    schema_editor.execute(sql_drop_trigger)

class Migration(migrations.Migration):

    dependencies = [
        # Укажите зависимости от предыдущих миграций
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_trigger, remove_trigger),
    ]

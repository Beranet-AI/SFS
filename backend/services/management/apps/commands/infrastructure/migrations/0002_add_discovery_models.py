from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("commands", "0001_initial"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            CREATE TABLE commands_discovery_session (
                id UUID PRIMARY KEY,
                edge_node_id VARCHAR(64) NOT NULL,
                status VARCHAR(16) NOT NULL,
                started_by VARCHAR(64) NOT NULL DEFAULT '',
                started_at TIMESTAMPTZ NOT NULL,
                finished_at TIMESTAMPTZ NULL,
                device_count INTEGER NOT NULL DEFAULT 0,
                error_message TEXT NOT NULL DEFAULT '',
                command_id UUID NULL,
                CONSTRAINT commands_discovery_session_command_fk
                    FOREIGN KEY (command_id)
                    REFERENCES commands_command(id)
                    ON DELETE SET NULL
            );
            """,
            reverse_sql="DROP TABLE commands_discovery_session;",
        ),
        migrations.RunSQL(
            sql="""
            CREATE TABLE commands_discovered_device (
                id UUID PRIMARY KEY,
                device_id VARCHAR(128) NOT NULL,
                device_type VARCHAR(128) NOT NULL DEFAULT '',
                ip_address VARCHAR(64) NOT NULL DEFAULT '',
                capabilities JSONB NOT NULL DEFAULT '{}'::jsonb,
                raw_payload JSONB NOT NULL DEFAULT '{}'::jsonb,
                status VARCHAR(16) NOT NULL,
                created_at TIMESTAMPTZ NOT NULL,
                updated_at TIMESTAMPTZ NOT NULL,
                registered_device_id UUID NULL,
                session_id UUID NOT NULL,
                CONSTRAINT commands_discovered_device_session_fk
                    FOREIGN KEY (session_id)
                    REFERENCES commands_discovery_session(id)
                    ON DELETE CASCADE
            );
            """,
            reverse_sql="DROP TABLE commands_discovered_device;",
        ),
    ]

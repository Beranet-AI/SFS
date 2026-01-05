from .command_model import CommandModel


class CommandResultModel(CommandModel):
    class Meta:
        proxy = True
        app_label = "commands"
        verbose_name = "Command Result"
        verbose_name_plural = "Command Results"

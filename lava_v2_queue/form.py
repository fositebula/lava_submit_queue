from django.forms import ModelForm, forms
from models import VerifyData, VerifyDataTmp


class VerifyDataForm(ModelForm):
    class Meta:
        model = VerifyData
        fields = ["buildlist", "build_id", "submit_user", "verify_url", "gerrit_id",
                  "port", "compile_user", "module", "test_cases", "manual_test_case",
                  "phone_number", "test_description", "project_num", "test_task_type"]

class VerifyDataTmpForm(ModelForm):
    class Meta:
        model = VerifyDataTmp
        fields = ["branch", "project", "build_id", "submit_user", "verify_url", "gerrit_id",
                  "port", "compile_user", "module", "test_cases", "manual_test_case",
                  "phone_number", "test_description", "project_num", "test_task_type"]

class RunningLogTmpForm(ModelForm):
    class Meta:
        model = VerifyDataTmp
        fields = ["id", "lavaJobId", "submitted_flag"]

    def save(self, commit=True):
        self.submitted_flag = 1
        self.full_clean()
        return super(RunningLogTmpForm, self).save()
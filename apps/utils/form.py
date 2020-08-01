class FormMixin(object):
    def get_errors(self):
        errors = self.errors.get_json_data()
        error_list = []
        for key, message_dicts in errors.items():
            for message in message_dicts:
                error_list.append(message['message'])
        return error_list

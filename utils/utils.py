import json


def get_message(message, options=None, msg_type='success'):
    """
    Печатает сообщение (уведомительные или ошибки).
    :message
    :param options словарь с ключами. Поддерживаются следующие ключи-опции:
        data - 
        absent_fields - 
        timeout - 
        location - 
        title - 
    :param msg_type - error или success
    :return: JSON-сообщение, отправляемое клиенту
    """
    res = {
        'data': [],
        'success': '1' if msg_type == 'success' else '0',
        'message': message,
    }
    res.update(options or {})
    return json.dumps(res);


def get_error(message, options=None):
    return get_message(message, options, 'error')


def get_success(message, options=None):
    return get_message(message, options, 'success')


# https://vk.com/dev/widgets_for_sites
# https://apiok.ru/ext/like
class VKTools:
    def get_widget_js(widgets):
        if 'share' in widgets:
            return ""

    def echo_share_button(text='Поделиться'):
            return ""


def get_absent_fields_list(form):
    absent_fields = []
    msg_err = []
    if form.errors:
        for field in form:
            if field.errors:
                absent_fields.append(field.name)
                msg_err.append('; '.join(field.errors))
        if form.non_field_errors:
            msg_err.extend('; '.join(form.non_field_errors()))
    return absent_fields, '<br'.join(msg_err)
<%inherit file="${context['main_template'].uri}" />
<%block name='actionmenucontent'>
% if request.has_permission("edit.project", layout.current_project_object):
<div class='layout flex main_actions'>
    <div role='group'>
        <a class='btn btn-primary icon' href="${layout.edit_url}">
            <svg><use href="${request.static_url('caerp:static/icons/endi.svg')}#pen"></use></svg>Modifier le dossier
        </a>
    </div>
</div>
% endif
</%block>



<%block name='mainblock'>
<div id="vue-file-app-container"></div>
</%block>
<%block name='footerjs'>
var AppOption = AppOption || {};
% for option, value in js_app_options.items():
${api.write_js_app_option(option, value)}
% endfor
</%block>
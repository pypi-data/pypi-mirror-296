<%inherit file="${context['main_template'].uri}" />

<%block name='mainblock'>
<div id="vue-file-app-container"></div>
</%block>
<%block name='footerjs'>
var AppOption = AppOption || {};
% for option, value in js_app_options.items():
${api.write_js_app_option(option, value)}
% endfor
</%block>
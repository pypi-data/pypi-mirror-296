<%doc>
Template listant les ateliers :

Atelier de la cae
Liste globale des formations
Liste des ateliers d'une enseigne
Liste des ateliers d'un utilisateur
Liste des formations d'une enseigne

</%doc>
<%inherit file="${context['main_template'].uri}" />
<%namespace file="/base/pager.mako" import="pager"/>
<%namespace file="/base/pager.mako" import="sortable"/>
<%namespace file="/base/utils.mako" import="show_tags_label" />
<%namespace file="/base/utils.mako" import="company_internal_msg" />
<%namespace file="/base/utils.mako" import="company_list_badges" />
<%namespace file="/base/searchformlayout.mako" import="searchform"/>

<%block name='actionmenucontent'>
% if ((request.has_permission('add.workshop') or request.has_permission('add.training')) and is_edit_view) or is_admin_view:
    <div class='layout flex main_actions'>
        <div role='group'>
        % if (request.has_permission('add.workshop') or request.has_permission('add.training')) and is_edit_view:
            % if request.has_permission('manage') and request.context .__name__ != 'company':
                <% url=request.route_path('workshops', _query=dict(action='new')) %>
            % else:
                <% url=request.route_path('company_workshops', _query=dict(action='new'),  id=request.context.id) %>
            % endif
            <a class='btn btn-primary' href='${url}'>
                ${api.icon("plus")}
                Nouvel atelier
            </a>
        % endif
    	</div>
        % if is_admin_view:
            <div role='group'>
                <%
                ## We build the link with the current search arguments
                args = request.GET
                url_xls = request.route_path(route_name_root, file_format='.xls', _query=args) if not is_company \
                else request.route_path('company_workshops{file_format}', file_format='.xls',id=company_id, _query=args)
                url_ods = request.route_path(route_name_root, file_format='.ods', _query=args) if not is_company \
                else request.route_path('company_workshops{file_format}', file_format='.ods',id=company_id, _query=args)
                url_csv = request.route_path(route_name_root, file_format='.csv', _query=args) if not is_company \
                else request.route_path('company_workshops{file_format}', file_format='.csv',id=company_id, _query=args)
                %>
                <a class='btn icon_only_mobile' href='${url_xls}' title="Exporter les éléments de la liste au format Excel (xls)">
                    ${api.icon("file-excel")}
                    Excel
                </a>
                <a class='btn icon_only_mobile' href='${url_ods}' title="Exporter les éléments de la liste au format Open Document (ods)">
                    ${api.icon("file-spreadsheet")}
                    ODS
                </a>
                <a class='btn icon_only_mobile' href='${url_csv}' title="Exporter les éléments de la liste au format csv">
                    ${api.icon("file-csv")}
                    CSV
                </a>
            </div>
        % endif
    </div>
% endif
</%block>

<%block name='content'>

${searchform()}

<div>
    <div>
        ${records.item_count} Résultat(s)
    </div>
    <div class='table_container'>
    % if records:
        <table class="hover_table">
            <thead>
                <tr>
                    <th scope='col' class='col_status' title='Statut'><span class="screen-reader-text">Vous êtes inscrit ?</span></th>
                    <th scope="col" class="col_datetime">${sortable("Date", "datetime")}</th>
                    <th scope="col" class="col_text">Intitulé de l’atelier</th>
                    <th scope="col" class="col_text">Lieu</th>
                    <th scope="col" class="col_text">Gestion et animation</th>
                    <th scope="col">Nombre de participant(s)</th>
                    % if is_edit_view:
                        <th scope="col" class="col_text">Présence</th>
                    % else:
                        <th scope="col" class="col_text">Horaires</th>
                    % endif
                    <th scope="col" class="col_actions" title="Actions"><span class="screen-reader-text">Actions</span></th>
                </tr>
            </thead>
            <tbody>
    % else:
        <table>
            <tbody>
                <tr>
                    <td class="col_text"><em>Aucun atelier ne correspond à ces critéres</em></td>
                </tr>
    % endif
                % for workshop in records:
                    % if request.has_permission('edit.workshop', workshop):
                        <% _query=dict(action='edit') %>
                    % else:
                        ## Route is company_workshops_subscribed, the context is the company
                        <% _query=dict() %>
                    % endif
                    <% url = request.route_path('workshop', id=workshop.id, _query=_query) %>
                    % if request.has_permission('view.workshop', workshop):
                        <% onclick = "document.location='{url}'".format(url=url) %>
                        % if request.has_permission('edit.workshop', workshop):
                        <% tooltip_title = "Cliquer pour voir ou modifier l’atelier « " + workshop.name + " »" %>
                        % else:
                        <% tooltip_title = "Cliquer pour voir l’atelier « " + workshop.name + " »" %>
                        % endif
					% else :
						<% tooltip_title = "" %>
						<% onclick= "javascript:void(0);" %>
                    % endif
                    <tr>
                        % if current_user_id and workshop.is_participant(current_user_id):
                    		% if request.has_permission('view.workshop', workshop):
		                <td class="col_status" onclick="${onclick}" title="Vous êtes inscrit à cet atelier - ${tooltip_title}" aria-label="Vous êtes inscrit à cet atelier">
                        	% else :
        		        <td class="col_status" title="Vous êtes inscrit à cet atelier - ${tooltip_title}">
                        	% endif
                            <span class="icon status valid">
                                ${api.icon('check-circle')}
                            </span>
                            <span class="screen-reader-text">Vous êtes inscrit à cet atelier</span>
                        % else:
                        <td class="col_status" onclick="${onclick}" title="${tooltip_title}">
                    	% endif
                        </td>
                        <td class="col_datetime" onclick="${onclick}" title="${tooltip_title}">
	                       	${api.format_date(workshop.datetime)}
	                    </td>
                        <td class="col_text" onclick="${onclick}" title="${tooltip_title}">
                            ${workshop.name}
                            % if workshop.tags:
                                ${show_tags_label(workshop.tags)}
                            % endif
                        </td>
                        <td class="col_text" onclick="${onclick}" title="${tooltip_title}">
                            ${workshop.place}
                        </td>
                        <td class="col_text" onclick="${onclick}" title="${tooltip_title}">
                            <ul class="workshop-managers">
                                <li>
                                    % if workshop.company_manager:
                                        ${workshop.company_manager.name}
                                        ${company_list_badges(workshop.company_manager)}
                                    % endif
                                    % if workshop.company_manager is None:
                                        ${company_internal_msg()}
                                    % endif
                                    <span class="icon" title="Gestionnaire de l’atelier">${api.icon("key")}</span>
                                </li>
                                % for trainer in workshop.trainers:
                                    <li>${trainer.label}</li>
                                % endfor
                            </ul>
                        </td>
                        <td onclick="${onclick}" title="${tooltip_title}">
                          ${len(workshop.participants)}
                          % if workshop.max_participants > 0:
                          /${workshop.max_participants}
                          % endif
                        </td>
                    	% if request.has_permission('view.workshop', workshop) and not request.has_permission('edit.workshop', workshop):
                		<td class="col_text" onclick="${onclick}" title="${tooltip_title}">
                        % else :
                        <td class="col_text">
                        % endif
                            % if request.has_permission('edit.workshop', workshop):
                                <ul>
                                    % for timeslot in workshop.timeslots:
                                        <li class="timeslot">
                                            <% pdf_url = request.route_path("timeslot.pdf", id=timeslot.id) %>
                                            <a href="${pdf_url}" title="Cliquer pour télécharger la feuille d’émargement au format PDF">
	                                            <span class="icon">${api.icon('file-pdf')}</span>
                                                % if workshop.relates_single_day():
                                                    ${api.format_datetime(timeslot.start_time, timeonly=True)} → \
                                                    ${api.format_datetime(timeslot.end_time, timeonly=True)} \
                                                    (${api.format_duration(timeslot.duration)})
                                                % else:
                                                    Du ${api.format_datetime(timeslot.start_time)} au \
                                                    ${api.format_datetime(timeslot.end_time)} \
                                                    (${api.format_duration(timeslot.duration)})
                                                % endif
                                            </a>
                                        </li>
                                    % endfor
                                </ul>
                            % else:
                                % for user in current_users:
                                    <% is_participant = workshop.is_participant(user.id) %>
                                    % if is_participant:
                                        ${api.format_account(user)} :
                                        % for timeslot in workshop.timeslots:
                                            <div>
                                                % if workshop.relates_single_day():
                                                    ${api.format_datetime(timeslot.start_time, timeonly=True)} → \
                                                    ${api.format_datetime(timeslot.end_time, timeonly=True)} : \
                                                % else:
                                                    Du ${api.format_datetime(timeslot.start_time)} \
                                                    au ${api.format_datetime(timeslot.end_time)} : \
                                                % endif
                                                ${timeslot.user_status(user.id)}
                                            </div>
                                        % endfor
                                    % endif
                                % endfor
                            % endif
                        </td>
                        ${request.layout_manager.render_panel('action_buttons_td', links=stream_actions(workshop))}
                    </tr>
                % endfor
            </tbody>
        </table>
    </div>
    ${pager(records)}
</div>
</%block>

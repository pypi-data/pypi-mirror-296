<%inherit file="${context['main_template'].uri}" />
<%doc>
Template de base pour l'onglet Vue générale d'un document
</%doc>

<%block name='mainblock'>
    <% current_task = request.context %>
            <%block name='before_summary'/>
			<div class="layout flex two_cols separate_bottom">
				<div>
					<h3>Informations générales</h3>
					<dl class='dl-horizontal'>
						<dt>Statut</dt>
						<dd>
							<span class="icon status  ${current_task.global_status}">
								${api.icon(api.status_icon(current_task))}
							</span>
							${api.format_status(current_task)}
						</dd>
						% if current_task.business is not None and current_task.business.visible:
							<dt>Affaire</dt>
							<dd><a href="${request.route_path('/businesses/{id}/overview', id=current_task.business_id)}">${current_task.business_type.label} : ${current_task.business.name}</a></dd>
						% elif current_task.business_type and current_task.business_type.name != 'default':
							<dt>Affaire de type</dt>
							<dd>${current_task.business_type.label}</dd>
						% endif
						<dt>Nom du document</dt>
						<dd>${current_task.name}</dd>
						<dt>Date</dt>
						<dd>${api.format_date(current_task.date)}</dd>
						<dt>Client</dt>
						<dd>
							<a href="${request.route_path('customer', id=current_task.customer.id)}" title="Voir la fiche du client" aria-label="Voir la fiche du client">
								<span class='icon'>${api.icon('address-card')}</span>${current_task.customer.label}
								% if current_task.customer.code:
									<small>(${current_task.customer.code})</small>
								% endif
							</a>
							% if current_task.customer.email:
							<br />
							<a href="mailto:${current_task.customer.email}" title="Envoyer un mail au client" aria-label="Envoyer un mail au client">
								<span class='icon'>${api.icon('envelope')}</span>${current_task.customer.email}
							</a>
							% endif
						</dd>
						<dt>Montant HT</dt>
						<dd>${api.format_amount(current_task.ht, precision=5)}&nbsp;€</dd>
						<dt>TVA</dt>
						<dd>${api.format_amount(current_task.tva, precision=5)}&nbsp;€ </dd>
						<dt>TTC</dt>
						<dd>${api.format_amount(current_task.ttc, precision=5)}&nbsp;€</dd>
					</dl>
					<%block name='after_summary' />
				</div>

                <!-- will get replaced by backbone -->
            	<div class="status_history"></div>
			</div>
             % if indicators:
                <div class="separate_bottom">
                    <h3>Indicateurs</h3>
                    <div class="table_container">
                        <table>
                            <thead>
                                <tr>
                                    <th scope="col" class="col_status" title="Statut"><span
                                            class="screen-reader-text">Statut</span></th>
                                    <th scope="col" class="col_text">Libellé</th>
                                    <th scope="col" class="col_actions width_one" title="Actions">
                                        <span class="screen-reader-text">Actions</span>
                                    </th>
                                </tr>
                            </thead>
                            <tbody>

                                <tr>
                                    <% file_status=current_task.get_file_requirements_status() %>
                                        <td class="col_status">
                                            <span class='icon status ${api.indicator_status_css(file_status)}'>
                                                ${api.icon(api.indicator_status_icon(file_status))}
                                            </span>
                                        </td>

                                        <td class="col_text">
                                            % if status == 'danger':
                                            Des documents sont manquants
                                            % elif status == 'warning':
                                            Des documents sont recommandés
                                            % else:
                                            Tous les fichiers ont été fournis
                                            % endif
                                        </td>
                                        <td class='col_actions width_one'>
                                            ${request.layout_manager.render_panel(file_tab_link.panel_name,
                                            context=file_tab_link)}
                                        </td>
                                </tr>
                            </tbody>
                        </table>

                    </div>
                </div>
                % endif
		</div>
        </%block>

<%inherit file="/tasks/general.mako" />

<%block name='before_summary'>
<% estimation = request.context %>
% if api.has_permission('set_signed_status.estimation'):
	<div class="separate_bottom content_vertical_padding">
		<% signed_status_url = request.route_path('/api/v1/estimations/{id}', id=estimation.id, _query={'action': 'signed_status'}) %>
		<div class="icon_choice layout flex signed_status_group" data-toggle="buttons" data-url="${signed_status_url}">
			% for action  in actions:
				<label
					class="${action.options['css']} ${'active' if estimation.signed_status == action.name else ''}"
					title="${'' if estimation.signed_status == action.name else 'Changer le statut en :'} ${action.options['label']}"
					>
					<input
						type="radio"
						title="${action.options['title']}"
						name="${action.status_attr}"
						value="${action.name}"
						autocomplete="off"
						class="visuallyhidden"
						% if estimation.signed_status == action.name:
							checked="checked"
						% endif
						>
						<span>
							<svg><use href="/static/icons/endi.svg#${action.options['icon']}"></use></svg>
							<span>${action.options['label']}</span>
							<span class="screen-reader-text"> (${'' if estimation.signed_status == action.name else 'Changer le statut en :'} ${action.options['label']})</span>
						</span>
				</label>
			% endfor
		</div>
	</div>
% endif
% if estimation.invoices:
	<div class="separate_bottom content_vertical_padding">
		<h3>
			Factures
			<% attach_invoices_url = request.route_path('/estimations/{id}/attach_invoices', id=estimation.id) %>
			<a class="btn icon only unstyled" title="Rattacher une facture" aria-label="Rattacher une facture" href="${attach_invoices_url}">
				<svg><use href="/static/icons/endi.svg#link"></use></svg>
			</a>
		</h3>
		<ul>
			% for invoice in estimation.invoices:
				<li>
					La facture (${api.format_invoice_status(invoice, full=False)})&nbsp;: \
					<a href="${api.task_url(invoice, suffix='/general')}">
						${invoice.internal_number}
						% if invoice.official_number:
							(${invoice.official_number})
						% endif
					</a>
					a été générée depuis ce devis.
				</li>
			% endfor
		</ul>
	</div>
% endif
</%block>

<%block name='after_summary'>
<% estimation = request.context %>
    % if estimation.internal and estimation.supplier_order and api.has_permission('view.supplier_order', estimation.supplier_order):
    <dl class='dl-horizontal'><dt>Devis interne</dt>
    <dd>
    <a
        href='${request.route_path("/supplier_orders/{id}", id=estimation.supplier_order_id)}'
        title="Voir la commande fournisseur"
        aria-label="Voir la commande fournisseur"
        >
        Voir la commande fournisseur associée
    </a>
    </dd>
    </dl>
    % endif
</%block>

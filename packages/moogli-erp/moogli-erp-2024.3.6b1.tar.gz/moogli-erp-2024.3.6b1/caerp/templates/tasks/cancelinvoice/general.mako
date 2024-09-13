<%inherit file="/tasks/general.mako" />

<%block name='before_summary'>
    <% cancelinvoice = request.context %>
	% if cancelinvoice.invoice:
    <div class="separate_bottom content_vertical_padding">
        <h4>
			Facture de référence :
			<a href="${api.task_url(cancelinvoice.invoice, suffix='/general')}">
			    ${cancelinvoice.invoice.official_number}
			</a>
		</h4>
        <div class='alert'>
            Cette facture d'avoir est rattachée à l’année fiscale ${cancelinvoice.financial_year}
            % if api.has_permission('set_treasury.cancelinvoice'):
                <a href="${api.task_url(cancelinvoice, suffix='/set_treasury')}" class="btn icon unstyled" title="Modifier l’année fiscale" aria-label="Modifier l’année fiscale">
                    <svg><use href="${request.static_url('caerp:static/icons/endi.svg')}#pen"></use></svg>
                    Modifier
                </a>
            % endif
        </div>
	</div>
	% else:
	<div class='alert alert-danger'>
		<span class="icon"><svg><use href="${request.static_url('caerp:static/icons/endi.svg')}#danger"></use></svg></span>
		Cet avoir n’est attaché à aucune facture (cela ne devrait pas se produire)
	</div>
	% endif
</%block>

<%block name='after_summary'>
    <% invoice = request.context %>
    
        
    % if invoice.internal and \
        invoice.supplier_invoice and \
        api.has_permission('view.supplier_invoice', invoice.supplier_invoice):
    <dl class='dl-horizontal'>
        <dt>Facture interne</dt>
        <dd>
            <a href='${request.route_path("/supplier_invoices/{id}", id=invoice.supplier_invoice_id)}' title="Voir la facture fournisseur" aria-label="Voir la facture fournisseur">
                Voir la facture fournisseur associée
            </a>
        </dd>
    </dl>
    % endif
    % if hasattr(next, 'invoice_more_data'):
        ${next.invoice_more_data()}
    % endif
</%block>
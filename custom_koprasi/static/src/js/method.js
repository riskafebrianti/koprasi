odoo.define('custom_koprasi.custom_payment_lines', function (require) {
    "use strict";

    var PaymentScreenPaymentLines = require('point_of_sale.PaymentScreenPaymentLines');
    var Registries = require('point_of_sale.Registries');
	var rpc = require('web.rpc')
    var Gui = require('point_of_sale.Gui');
    var core = require('web.core');
    var _t = core._t;

    const CustomPaymentLines = (PaymentScreenPaymentLines) =>
        class extends PaymentScreenPaymentLines {
            async selectedLineClass(line) {
                console.log(line.name);
                const partner = line.order.get_partner();
                const originalClassUnselect = super.unselectedLineClass(line);
                let idrFormat = new Intl.NumberFormat('id-ID', {
                    style: 'currency',
                    currency: 'IDR',
                    minimumFractionDigits: 0,  // No decimal places for IDR
                });

                    if  (line.name == 'Customer Account'){
                        const limits = line.amount + partner.credit_limit
                        // console.log(partner.credit_limit)
                        // console.log(line)
                        // console.log(limits)
                        if (limits > partner.limit){
                            const keterangan = "Total Limit " + partner.name + " adalah " + idrFormat.format(partner.limit) + ", Silahkan Gunakan Metode Pembayaran Lainnya"
                            // console.log("YUKK BISA YUKK")

                            const { confirmed } = await this.showPopup("ConfirmPopup", {
                                title : this.env._t('Pembelian Lebih dari Limit Anggota'),
                                body : this.env._t(keterangan),
                                confirmText: this.env._t("OK"),
                                // cancelText: this.env._t("Cancel"),
                            });
                            if (confirmed) {
                                // console.log("User menekan OK");
                                line.order.remove_paymentline(line);
                                // Tambahkan aksi lain jika perlu
                            } 
                            else{
                                line.order.remove_paymentline(line);
                            }
                        }
                        // else{
                            
                        //     // const originalClass = super.selectedLineClass(line);
            
                        //     // Tambahkan kustomisasi (misal: tambahkan kelas CSS tambahan)
                        //     // return Object.assign({}, originalClassUnselect, { 'custom-selected': true });
                        // }
                    }
                
                // Panggil fungsi asli agar tetap berfungsi
            }

            
        };

    Registries.Component.extend(PaymentScreenPaymentLines, CustomPaymentLines);

    return CustomPaymentLines;
});
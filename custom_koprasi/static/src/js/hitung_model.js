/** @odoo-modules */

import {Order, Orderline, PosGlobalState} from 'point_of_sale.models';
import Registries from 'point_of_sale.Registries';


// const OrderInherit = (Order) => class OrderInherit extends Order {
const OrderlineInherit = (Orderline) => class OrderlineInherit extends Orderline {
    

    export_as_JSON() {
        const json = super.export_as_JSON(...arguments);
        json.harga = this.harga
        return json;
    }

    init_from_JSON(json) {
        super.init_from_JSON(...arguments);
        this.harga = json.harga;
    }

   
    inputHarga(harga) {
        this.harga = harga;
    }
}

Registries.Model.extend(Orderline, OrderlineInherit);
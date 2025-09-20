// Copyright (c) 2025, keerthana and contributors
// For license information, please see license.txt

frappe.ui.form.on("Booking", {
	type: function(frm){
	  frm.set_query("resource", function() {
	      return {
	          filters: {
	              type: frm.doc.type,
								availability : "Available"
	          }
	      };
	  });
	}
});

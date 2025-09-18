# Copyright (c) 2025, keerthana and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _
from frappe.utils import get_datetime

class Booking(Document):

    def validate(self):
        self.validate_booking()

    def autoname(self):
	    """Generate Booking ID automatically"""
	    if self.resource and self.user and self.posting_date:
	        posting_date_str = self.posting_date
	        user_str = (self.user or "").replace(" ", "").lower()
	        self.name = f"{self.resource}-{user_str}-{posting_date_str}"
	    else:
	        frappe.throw(_("Resource, User, and Posting Date are required to generate Booking ID"))


    def validate_booking(self):
        if frappe.db.exists(
            "Booking",
            {
                "resource": self.resource,
                "start_time": self.start_time,
                "end_time": self.end_time,
                "status": "Approved",
            },
        ):
            frappe.throw(_("Resource {0} is already booked for this time slot").format(self.resource))

# Copyright (c) 2025, keerthana and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _
from frappe.utils import get_datetime
import hashlib

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
        """Validate Booking """
        overlapping = frappe.db.sql("""
            SELECT name
            FROM `tabBooking`
            WHERE resource = %(resource)s
              AND status IN ('Approved', 'Pending')
              AND name != %(name)s
              AND (
                    (start_time < %(end_time)s AND end_time > %(start_time)s)
                  )
        """, {
            "resource": self.resource,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "name": self.name or "New Booking"
        }, as_dict=True)

        if overlapping:
            frappe.throw(
                _("Resource {0} is already booked during this time slot").format(self.resource)
            )


@frappe.whitelist()
def get_booking_events(start, end, filters=None):
    """Get Booking Details for Calender View """
    events = []
    booking_plans = frappe.get_all(
        "Booking",
        fields=["name", "type", "resource", "user", "start_time", "end_time", "posting_date"],
        filters={"posting_date": ["between", [start, end]]}
    )

    for booking in booking_plans:
        color = "#" + hashlib.md5(booking.type.encode()).hexdigest()[:6]
        events.append({
            "id": booking.name,
            "title": f"{booking.user} ({booking.type})",
            "start": booking.start_time,
            "end": booking.end_time,
            "color": color
        })

    return events

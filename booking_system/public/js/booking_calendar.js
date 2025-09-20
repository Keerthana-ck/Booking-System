frappe.views.calendar["Booking"] = {
    field_map: {
        "start": "start_time",
        "end": "end_time",
        "id": "name",
        "title": "title"
    },
    options: {
        header: {
            left: "prev,next today",
            center: "title",
            right: "month,agendaWeek,agendaDay"
        }
    },
    get_events_method: "booking_system.booking_system.doctype.booking.booking.get_booking_events"
};

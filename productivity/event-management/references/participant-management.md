# Participant CSV Import & Curation Flow

## Import Sequence
1. **Export**: Extract CSV from event platform (Luma, Eventbrite, etc.).
2. **Mapping**: Map platform columns to Notion DB properties (e.g., `first_name` + `last_name` $\rightarrow$ `Name (Title)`).
3. **Import**: Use Notion's CSV import to append to existing Participant DB.
4. **Deduplication**: Clean duplicates based on `email` or `guest_id`.
5. **Curation (Crucial)**: Manually assign `Attendee Attribute`, `Industry`, and `Attendance Type` based on organization names and roles.

## Curation Priority
1. Sponsors $\rightarrow$ 2. Speakers $\rightarrow$ 3. VIPs $\rightarrow$ 4. Media $\rightarrow$ 5. General Attendees

## Reporting Summary Template
- Total Registered: [Count]
- Approved: [Count] | Invited: [Count] | Pending: [Count]
- Top Industries: [List top 3-5]
- Key Organizations: [List top 5-10]
- Net Revenue: [Total]

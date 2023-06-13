# DÖKBackend DB Schema
- ## Users
    - user_id [uuid]
        - name [string]
        - joined_at [timestamp]
        - auth_level [int]

- ## Doors
    - door_id [uuid]
        - name [string]
        - auth_level_needed [int]

- ## DoorAccess
    - access_id [uuid]
        - user_id [uuid]
        - door_id [uuid]
        - accessed_at [timestamp]

- ## News
    - news_id [uuid]
        - author_id [uuid]
        - created_at [timestamp]
        - content [string]

- ## Tasks
    - task_id [uuid]
        - author_id [uuid]
        - assigned_to [uuid] *(can be multiple)*
        - description [string]
        - deadline [timestamp]

- ## Votes
    - vote_id [uuid]
        - author_id [uuid]
        - content [string]
        - vote_y [int]
        - vote_n [int]
        - vote_total [int] *(calculated from 0+vote_y-vote_n)*

- ## Chat
    - message_id [uuid]
        - author_id [uuid]
        - sent_at [timestamp]
        - content [string]

@aerthexv(
    name="User Activity Tracker", 
    author="Luxed",
    description="Track specific users' activity across all servers or dms", 
    usage="UI Script (v1.1)"
)
def userActivityTracker():
    def updateUserActivitySettings(key, value):
        file_path = f'{getScriptsPath()}/userActivity.json'
        try:
            with open(file_path, 'r', encoding="utf-8") as file:
                settings = json.load(file)
        except FileNotFoundError:
            settings = {"tracked_users": [], "selected_events": []}
        settings[key] = value
        with open(file_path, 'w', encoding="utf-8") as file:
            json.dump(settings, file, indent=2)

    def getUserActivitySettings(key=None):
        try:
            with open(f'{getScriptsPath()}/userActivity.json', 'r') as file:
                settings = json.load(file)
        except FileNotFoundError:
            settings = {
                "tracked_users": [],
                "selected_events": [],
                "excluded_servers": []  
            }
        if key:
            return settings.get(key)
        return settings

    def getTimeDetails():
        now = datetime.now()
        return {
            "text": now.strftime("%d %B %Y"),
            "subtext": now.strftime("at %H:%M:%S")
        }

    bot.ua_selected_rows = []

    def updateTableSelection(selected):
        bot.ua_selected_rows = selected
        if bot.ua_selected_rows:
            ua_delete_selected.disabled = False
        else:
            ua_delete_selected.disabled = True

    def deleteSelectedClick():
        ua_activity_table.delete_rows(bot.ua_selected_rows)
        ua_delete_selected.disabled = True

    ua_tab = Tab(name='User Activity', title="User Activity Tracker", icon="users")
    ua_container = ua_tab.create_container(type="rows")
    ua_card = ua_container.create_card(height="full", width="full", gap=3)

    ua_top_group = ua_card.create_group(type="columns", gap=3, full_width=True)
    ua_input = ua_top_group.create_ui_element(UI.Input, label="Enter User ID", full_width=True, show_clear_button=True, required=True)
    ua_add_button = ua_top_group.create_ui_element(UI.Button, label='Add User', disabled=True, full_width=False, color="primary")

    events_select_list = [
    {"id": "message_sent", "title": "Message Sent", "color": "blue"},
    {"id": "message_edited", "title": "Message Edited", "color": "yellow"},
    {"id": "message_deleted", "title": "Message Deleted", "color": "red"},
    {"id": "reaction_added", "title": "Reaction Added", "color": "purple"},
    {"id": "reaction_removed", "title": "Reaction Removed", "color": "purple"},
    {"id": "voice_joined", "title": "Voice Joined", "color": "green"},
    {"id": "voice_left", "title": "Voice Left", "color": "orange"},
    {"id": "nickname_change", "title": "Nickname Change", "color": "pink"},
    {"id": "role_update", "title": "Role Update", "color": "cyan"},
    {"id": "guild_join", "title": "Server Join", "color": "green"},
    {"id": "guild_remove", "title": "Server Leave", "color": "red"},
    {"id": "thread_created", "title": "Thread created", "color": "orange"},
    {"id": "thread_deleted", "title": "Thread deleted", "color": "red"}
    ]

    servers_select_list = [{"id": "select_server", "title": "Select server(s)", "disabled": True}]
    excluded_servers = getUserActivitySettings("excluded_servers") or []
    
    for excluded_id in excluded_servers:
        if excluded_id.startswith('dm_'):
            user_id = excluded_id.split('_')[1]
            user = bot.get_user(int(user_id))
            if user:
                servers_select_list.append({
                    "id": excluded_id,
                    "title": f"DM with {user.display_name}",
                    "iconUrl": str(user.display_avatar.url)
                })

    for server in bot.guilds:
        servers_select_list.append({
            "id": str(server.id),
            "title": server.name,
            "iconUrl": str(server.icon.url) if server.icon else "https://cdn.discordapp.com/embed/avatars/0.png"
        })

    def updateExcludedServers(selected: list):
        updateUserActivitySettings("excluded_servers", selected)

    ua_server_select = ua_top_group.create_ui_element(
        UI.Select,
        label="Exclude Servers",
        items=servers_select_list,
        mode="multiple",
        disabled_items=['select_server'],
        selected_items=getUserActivitySettings("excluded_servers"),
        onChange=updateExcludedServers
    )

    def updateSelectedEvents(selected: list):
        valid_events = [event["id"] for event in events_select_list if event["id"] != "select_event"]
        filtered_selected = [item for item in selected if item in valid_events]
        updateUserActivitySettings("selected_events", filtered_selected)

    ua_events_select = ua_top_group.create_ui_element(
        UI.Select,
        label="Select Events",
        items=events_select_list,
        mode="multiple",
        disabled_items=['select_event'],
        selected_items=getUserActivitySettings("selected_events"),
        onChange=updateSelectedEvents
    )
    
    ua_delete_selected = ua_top_group.create_ui_element(
        UI.Button, 
        variant="ghost", 
        label='Delete selected logs', 
        disabled=True, 
        full_width=False, 
        color="danger", 
        onClick=deleteSelectedClick,
    )

    ua_table_group = ua_card.create_group(type="columns", gap=6, full_width=True, horizontal_align="center")
    
    def removeTrackedUser(row_id: str):
        settings = getUserActivitySettings()
        if row_id in settings["tracked_users"]:
            settings["tracked_users"].remove(row_id)
            updateUserActivitySettings("tracked_users", settings["tracked_users"])
            ua_users_table.delete_rows([row_id])
            ua_tab.toast(type="SUCCESS", title="Deleted user", description=f"The user with ID {row_id} has been removed from the tracker.")

    ua_users_table = ua_table_group.create_ui_element(UI.Table, 
        selectable=False,
        search=True,
        items_per_page=5,
        columns=[
            {"type": "text", "label": "User"},
            {"type": "text", "label": "User ID"},
            {"type": "button", "label": "Actions", "buttons": [
                {"label": "Remove", "color": "danger", "onClick": removeTrackedUser}
            ]}
        ],
        rows=[]
    )

    def getRow(row_id):
        return next((entry for entry in ua_activity_table.rows if entry["id"] == row_id), None)

    def jumpTo(row_id):
        row = getRow(row_id)
        if row:
            extras = row['cells'][-1]
            jump_url = extras.get('jump_to')
            if jump_url:
                try:
                    os.startfile(jump_url)
                except Exception as e:
                    ua_tab.toast(type="ERROR", title="Jump Error", description=f"The link could not be opened: {str(e)}")

    def enableServer(row_id):
        row = getRow(row_id)
        if row:
            extras = row['cells'][-1]
            server_id = extras.get('server_id')
            if server_id:
                excluded_servers = getUserActivitySettings("excluded_servers") or []
                if server_id in excluded_servers:
                    excluded_servers.remove(server_id)
                    updateUserActivitySettings("excluded_servers", excluded_servers)
                    ua_server_select.selected_items = excluded_servers
                    ua_tab.toast(type="SUCCESS", title="Server enabled", description=f"Tracking enabled for the server {extras['server_id']}")

    def disableServer(row_id):
        row = getRow(row_id)
        if row:
            extras = row['cells'][-1]
            excluded_servers = getUserActivitySettings("excluded_servers") or []
            
            exclusion_id = (
                f"dm_{extras['jump_to']['user_id']}" 
                if 'user_id' in extras.get('jump_to', {}) 
                else str(extras.get('server_id', ''))
            )
            
            if exclusion_id and exclusion_id not in excluded_servers:
                excluded_servers.append(exclusion_id)
                updateUserActivitySettings("excluded_servers", excluded_servers)
                ua_server_select.selected_items = excluded_servers
                
                if exclusion_id.startswith('dm_'):
                    user = bot.get_user(int(exclusion_id.split('_')[1]))
                    target_name = f"DM with {user.display_name}" if user else "Deleted User"
                else:
                    guild = bot.get_guild(int(exclusion_id))
                    target_name = guild.name if guild else f"Server {exclusion_id}"
                
                ua_tab.toast(type="SUCCESS", title="Tracking Disabled", description=f"Stopped tracking in: {target_name}")

    def disableEvent(row_id):
        row = getRow(row_id)
        if row:
            extras = row['cells'][-1]
            event_type = extras.get('event_type')
            if event_type:
                current_selected = getUserActivitySettings("selected_events") or []
                if event_type in current_selected:
                    new_selected = [e for e in current_selected if e != event_type]
                    updateSelectedEvents(new_selected)
                    ua_events_select.selected_items = new_selected
                    ua_tab.toast(type="INFO", title="Event disabled", description=f"Tracking disabled for {event_type} events")

    ua_activity_table = ua_table_group.create_ui_element(UI.Table,
        selectable=False,
        search=True,
        items_per_page=10,
        columns=[
            {"type": "tag", "label": "Type"},
            {"type": "text", "label": "User"},
            {"type": "text", "label": "Details"},
            {"type": "text", "label": "Time"},
            { 
                "type": "button", 
                "label": "Actions", 
                "buttons": [
                    {"label": "Jump", "color": "default", "onClick": jumpTo},
                    {"label": "Disable server", "color": "danger", "onClick": disableServer},
                    {"label": "Enable server", "color": "default", "onClick": enableServer},
                    {"label": "Disable event", "color": "danger", "onClick": disableEvent},
                    {"label": "Copy to clipboard", "color": "default", "onClick": lambda row_id: pyperclip.copy(getRow(row_id)['cells'][2]['text'])}
                ]
            }
        ],
        rows=[]
    )

    ua_activity_table.onSelectionChange = updateTableSelection

    def format_custom_emojis(content, guild) -> str:
        """Handle both string-based message content and Emoji objects from reactions"""
        if isinstance(content, str):
            if not guild:
                return content
            pattern = re.compile(r'<(?P<animated>a?):(?P<name>\w+):(?P<id>\d+)>')
            return pattern.sub(r':\g<name>:', content)
        else:
            if hasattr(content, 'is_custom_emoji') and content.is_custom_emoji():
                return f":{content.name}:"
            return str(content)

    @bot.listen("on_message")
    async def trackMessageActivity(message):
        try:
            settings = getUserActivitySettings()
            server_id = str(message.guild.id) if message.guild else str(message.channel.id)
            
            if should_track_event(settings, message.author.id, "message_sent", server_id):
                user = await bot.fetch_user(message.author.id)
                content = process_message_content(message)
                
                insertActivityRow(**build_activity_data(
                    user=user,
                    event_type="message_sent",
                    server_name=message.guild.name if message.guild else "DM",
                    details=content,
                    extras={
                        'jump_to': {
                            'message_url': message.jump_url.replace("https://", "discord://"),
                            'guild_id': message.guild.id if message.guild else '0',
                            'channel_id': message.channel.id,
                            'message_id': message.id,
                            'user_id': message.author.id
                        }
                    }
                ))
        except Exception as e:
            pass

    @bot.listen("on_message_edit")
    async def trackMessageEdit(before, after):
        try:
            if before.content == after.content:
                return

            settings = getUserActivitySettings()
            server_id = str(after.guild.id) if after.guild else str(after.channel.id)
            
            if should_track_event(settings, after.author.id, "message_edited", server_id):
                user = await bot.fetch_user(after.author.id)
                
                def format_edit_details(before_msg, after_msg):
                    before_content = process_message_content(before_msg) or "No content"
                    after_content = process_message_content(after_msg) or "No content"
                    return f"Original: {before_content}\nEdited: {after_content}"
                
                insertActivityRow(**build_activity_data(
                    user=user,
                    event_type="message_edited",
                    server_name=after.guild.name if after.guild else "DM",
                    details=format_edit_details(before, after),
                    extras={
                        'jump_to': {
                            'message_url': after.jump_url.replace("https://", "discord://"),
                            'guild_id': after.guild.id if after.guild else '',
                            'channel_id': after.channel.id,
                            'message_id': after.id,
                            'user_id': user.id
                        }
                    }
                ))
        except Exception as e:
            pass

    @bot.listen("on_message_delete")
    async def trackMessageDelete(message):
        try:
            settings = getUserActivitySettings()
            server_id = str(message.guild.id) if message.guild else  str(message.channel.id)
            
            if should_track_event(settings, message.author.id, "message_deleted", server_id):
                user = await bot.fetch_user(message.author.id)
                
                insertActivityRow(**build_activity_data(
                    user=user,
                    event_type="message_deleted",
                    server_name=message.guild.name if message.guild else "DM",
                    details=process_message_content(message),
                    extras={
                        'jump_to': {
                            'guild_id': message.guild.id if message.guild else '@me',
                            'channel_id': message.channel.id,
                            'message_id': message.id
                        }
                    }
                ))
        except Exception as e:
            pass

    @bot.listen("on_reaction_add")
    async def trackReactionAdd(reaction, user):
        try:
            settings = getUserActivitySettings()
            server_id = str(reaction.message.guild.id) if reaction.message.guild else str(reaction.message.channel.id)
            
            if should_track_event(settings, user.id, "reaction_added", server_id):
                fetched_user = await bot.fetch_user(user.id)
                emoji_text = format_custom_emojis(reaction.emoji, reaction.message.guild)
                
                insertActivityRow(**build_activity_data(
                    user=fetched_user,
                    event_type="reaction_added",
                    server_name=reaction.message.guild.name if reaction.message.guild else "DM",
                    details=f"Reaction: {emoji_text}",
                    extras={
                        'jump_to': {
                            'message_url': reaction.message.jump_url.replace("https://", "discord://"),
                            'guild_id': reaction.message.guild.id if reaction.message.guild else '0',  
                            'channel_id': reaction.message.channel.id,
                            'message_id': reaction.message.id
                        }
                    }
                ))
        except Exception as e:
            pass

    @bot.listen("on_reaction_remove")
    async def trackReactionRemove(reaction, user):
        try:
            settings = getUserActivitySettings()
            server_id = str(reaction.message.guild.id) if reaction.message.guild else str(reaction.message.channel.id)
            
            if should_track_event(settings, user.id, "reaction_removed", server_id):
                fetched_user = await bot.fetch_user(user.id)
                emoji_text = format_custom_emojis(reaction.emoji, reaction.message.guild)
                
                insertActivityRow(**build_activity_data(
                    user=fetched_user,
                    event_type="reaction_removed",
                    server_name=reaction.message.guild.name if reaction.message.guild else "DM",
                    details=f"Removed reaction: {emoji_text}",
                    extras={
                        'jump_to': {
                            'guild_id': reaction.message.guild.id if reaction.message.guild else '@me',
                            'channel_id': reaction.message.channel.id,
                            'message_id': reaction.message.id
                        }
                    }
                ))
        except Exception as e:
            pass

    @bot.listen("on_voice_state_update")
    async def trackVoiceActivity(member, before, after):
        try:
            settings = getUserActivitySettings()
            server_id = str(member.guild.id)
            
            event_type = None
            if not before.channel and after.channel:
                event_type = "voice_joined"
            elif before.channel and not after.channel:
                event_type = "voice_left"
            elif before.channel != after.channel:
                event_type = "voice_moved"
            
            if event_type and should_track_event(settings, member.id, event_type, server_id):
                user = await bot.fetch_user(member.id)
                channel = after.channel or before.channel
                details = f"Channel: {channel.name}" + (
                    f"\nMoved: {before.channel.name} → {after.channel.name}" 
                    if event_type == "voice_moved" else ""
                )
                
                insertActivityRow(**build_activity_data(
                    user=user,
                    event_type=event_type,
                    server_name=member.guild.name,
                    details=details,
                    extras={
                        'jump_to': {
                            'guild_id': member.guild.id,
                            'channel_id': channel.id,
                            'user_id': member.id,
                            'previous_channel_id': before.channel.id if before.channel else None
                        }
                    }
                ))
        except Exception as e:
            pass

    @bot.listen("on_member_update")
    async def trackNicknameChange(before, after):
        try:
            settings = getUserActivitySettings()
            server_id = str(after.guild.id)
            
            if (before.nick != after.nick and 
                should_track_event(settings, after.id, "nickname_change", server_id)):
                
                user = await bot.fetch_user(after.id)
                insertActivityRow(**build_activity_data(
                    user=user,
                    event_type="nickname_change",
                    server_name=after.guild.name,
                    details=f"From: {before.nick or before.display_name}\nTo: {after.nick or after.display_name}",
                    extras={
                        'jump_to': {
                            'guild_id': after.guild.id,
                            'user_id': user.id
                        }
                    }
                ))
        except Exception as e:
            pass

    @bot.listen("on_member_update")
    async def trackRoleChange(before, after):
        try:
            if before.roles == after.roles:
                return

            if not after.guild:
                return
                
            settings = getUserActivitySettings()
            server_id = str(after.guild.id)
            
            if should_track_event(settings, after.id, "role_update", server_id):
                user = await bot.fetch_user(after.id)
                added = [role for role in after.roles if role not in before.roles]
                removed = [role for role in before.roles if role not in after.roles]
                
                if added or removed:
                    def format_role_changes(added_roles, removed_roles):
                        changes = []
                        if added_roles:
                            roles = ", ".join([r.name for r in added_roles if r.name])
                            changes.append(f"Add: ({roles})" if roles else "")
                        if removed_roles:
                            roles = ", ".join([r.name for r in removed_roles if r.name])
                            changes.append(f"Remove: ({roles})" if roles else "")
                        return "\n".join(filter(None, changes)) or "Role changes could not be determined"

                    system_channel = after.guild.system_channel
                    
                    insertActivityRow(**build_activity_data(
                        user=user,
                        event_type="role_update",
                        server_name=after.guild.name,
                        details=format_role_changes(added, removed),
                        extras={
                            'jump_to': {
                                'guild_id': after.guild.id,
                                'user_id': after.id,
                                'channel_id': system_channel.id if system_channel else None
                            }
                        }
                    ))
        except Exception as e:
            pass

    @bot.listen("on_member_remove")
    async def trackGuildRemove(member):
        try:
            settings = getUserActivitySettings()
            server_id = str(member.guild.id)
            
            if should_track_event(settings, member.id, "guild_remove", server_id):
                user = await bot.fetch_user(member.id)
                insertActivityRow(**build_activity_data(
                    user=user,
                    event_type="guild_remove",
                    server_name=member.guild.name,
                    details="User left/kicked from server",
                    extras={
                        'jump_to': {
                            'guild_id': member.guild.id,
                            'user_id': user.id
                        }
                    }
                ))
        except Exception as e:
            pass

    @bot.listen("on_member_join")
    async def trackGuildJoin(member):
        try:
            settings = getUserActivitySettings()
            server_id = str(member.guild.id)
            
            if should_track_event(settings, member.id, "guild_join", server_id):
                user = await bot.fetch_user(member.id)
                insertActivityRow(**build_activity_data(
                    user=user,
                    event_type="guild_join",
                    server_name=member.guild.name,
                    details="Joined the server",
                    extras={
                        'jump_to': {
                            'guild_id': member.guild.id,
                            'user_id': user.id
                        }
                    }
                ))
        except Exception as e:
            pass

    @bot.listen("on_thread_create")
    async def trackThreadCreate(thread):
        try:
            settings = getUserActivitySettings()
            server_id = str(thread.guild.id) if thread.guild else "DM"
            
            if should_track_event(settings, thread.owner_id, "thread_created", server_id):
                user = await bot.fetch_user(thread.owner_id)
                parent_channel = f"#{thread.parent.name}" if thread.parent else "Unknown channel"
                
                insertActivityRow(**build_activity_data(
                    user=user,
                    event_type="thread_created",
                    server_name=thread.guild.name if thread.guild else "DM",
                    details=f"Thread: {thread.name}\nIn: {parent_channel}",
                    extras={
                        'jump_to': {
                            'channel_id': thread.id,
                            'guild_id': thread.guild.id if thread.guild else '',
                            'message_id': thread.id
                        }
                    }
                ))
        except Exception as e:
            pass

    @bot.listen("on_thread_delete")
    async def trackThreadDelete(thread):
        try:
            settings = getUserActivitySettings()
            server_id = str(thread.guild.id) if thread.guild else "DM"
            
            if should_track_event(settings, thread.owner_id, "thread_deleted", server_id):
                user = await bot.fetch_user(thread.owner_id)
                parent_channel = f"#{thread.parent.name}" if thread.parent else "Unknown channel"
                
                insertActivityRow(**build_activity_data(
                    user=user,
                    event_type="thread_deleted",
                    server_name=thread.guild.name if thread.guild else "DM",
                    details=f"Deleted thread: {thread.name}\nIn: {parent_channel}",
                    extras={
                        'jump_to': {
                            'guild_id': thread.guild.id if thread.guild else '',
                            'channel_id': thread.parent.id if thread.parent else ''
                        }
                    }
                ))
        except Exception as e:
            pass

    def insertActivityRow(user_id: int, user_name: str, avatar_url: str, event_type: str, server_name: str, details: str, extras: dict):
        settings = getUserActivitySettings()
        if str(user_id) in settings["tracked_users"] and event_type in settings["selected_events"]:
            event_config = next((e for e in events_select_list if e["id"] == event_type), None)
            
            if server_name == "DM":
                server_id = str(extras.get('jump_to', {}).get('channel_id', 'unknown'))
            else:
                guild = next((g for g in bot.guilds if g.name == server_name), None)
                server_id = str(guild.id) if guild else 'unknown'
            
            jump_data = extras.get('jump_to', {})
            final_extras = {
                "server_id": server_id,
                "event_type": event_type,
                "jump_to": generateJumpUrl(event_type, jump_data)
            }
            
            if server_name == "DM":
                final_extras['server_name'] = "DM"
            
            ua_activity_table.insert_rows([{
                "id": str(uuid.uuid4()),
                "cells": [
                    {
                        "text": event_config["title"] if event_config else event_type,
                        "color": event_config["color"] if event_config else "gray"
                    },
                    {
                        "text": user_name,
                        "imageUrl": avatar_url,
                        "subtext": f"Server: {server_name}"
                    },
                    {"text": details},
                    getTimeDetails(),
                    final_extras
                ]
            }])

    def should_track_event(settings: dict, user_id: str, event_type: str, server_id: str) -> bool:
        return (str(user_id) in settings["tracked_users"] and 
                event_type in settings["selected_events"] and
                server_id not in settings.get("excluded_servers", []))

    def build_activity_data(user: discord.User, event_type: str, server_name: str, details: str, extras: dict) -> dict:
        return {
            "user_id": user.id,
            "user_name": user.display_name,
            "avatar_url": str(user.display_avatar.url),
            "event_type": event_type,
            "server_name": server_name,
            "details": details,
            "extras": extras
        }

    def process_message_content(message: discord.Message) -> str:
        content = message.clean_content or ("Attachments" if message.attachments else "No content")
        content = format_custom_emojis(content, message.guild)
        
        if message.attachments:
            attachments = [
                f"📎 {a.filename} ({a.size//1024} KB)" 
                for a in message.attachments
            ]
            content += "\n" + "\n".join(attachments)
        
        return content

    def generateJumpUrl(event_type: str, data: dict) -> str:
        base_url = "discord://discord.com"
        
        url_patterns = {
            "message_sent": lambda d: d.get('message_url', f"{base_url}/channels/{d.get('guild_id', '')}/{d.get('channel_id', '')}/{d.get('message_id', '')}"),
            "message_edited": lambda d: d.get('message_url', f"{base_url}/channels/{d.get('guild_id', '')}/{d.get('channel_id', '')}/{d.get('message_id', '')}"),
            "message_deleted": lambda d: (f"{base_url}/channels/{d.get('guild_id', '@me')}/"f"{d.get('channel_id', '')}/"f"{d.get('message_id', '')}"),
            "reaction_added": lambda d: d.get('message_url', f"{base_url}/channels/{d.get('guild_id', '')}/{d.get('channel_id', '')}/{d.get('message_id', '')}"),
            "reaction_removed": lambda d: f"{base_url}/channels/{d.get('guild_id', '@me')}/"f"{d.get('channel_id')}/"f"{d.get('message_id')}",
            "voice_state_update": lambda d: f"{base_url}/channels/{d.get('guild_id', '')}/{d.get('channel_id', '')}",
            "nickname_change": lambda d: f"{base_url}/channels/{d.get('guild_id', '')}/{d.get('user_id', '')}",
            "role_update": lambda d: f"{base_url}/channels/{d.get('guild_id', '')}/{d.get('channel_id', '')}",
            "guild_remove": lambda d: f"{base_url}/channels/{d.get('guild_id', '')}/{d.get('user_id', '')}",
            "guild_join": lambda d: f"{base_url}/channels/{d.get('guild_id', '')}/{d.get('user_id', '')}",
            "thread_created": lambda d: f"{base_url}/channels/{d.get('guild_id', '')}/{d.get('channel_id', '')}",
            "thread_deleted": lambda d: f"{base_url}/channels/{d.get('guild_id', '')}/{d.get('channel_id', '')}"
        }
        
        return url_patterns.get(event_type, lambda _: f"{base_url}/users/{data.get('user_id', '')}")(data)

    async def addTrackedUser(user_id: str):
        try:
            user = await bot.fetch_user(int(user_id))
            settings = getUserActivitySettings()
            if user_id not in settings["tracked_users"]:
                settings["tracked_users"].append(user_id)
                updateUserActivitySettings("tracked_users", settings["tracked_users"])
                
                ua_users_table.insert_rows([{
                    "id": user_id,
                    "cells": [
                        {"text": user.display_name, "imageUrl": user.display_avatar.url},
                        {"text": user_id},
                        {}
                    ]
                }])
                ua_tab.toast(type="SUCCESS", title="User added", description=f"{user.display_name} has been added to the tracker.")
                ua_input.value = ""
            else:
                ua_tab.toast(type="INFO", title="User already exists", description="This user is already being tracked")
        except discord.NotFound:
            ua_input.invalid = True
            ua_input.error_message = "User not found"
            ua_tab.toast(type="ERROR", title="Error", description="User does not exist")
        except discord.HTTPException:
            ua_input.invalid = True
            ua_input.error_message = "Connection error"
            ua_tab.toast(type="ERROR", title="Error", description="User could not be verified")

    def validateUserID(new_value):
        if new_value == "":
            ua_input.invalid = False
            ua_input.error_message = None
            ua_add_button.disabled = True
        elif not new_value.isdigit() or len(new_value) < 17:
            ua_input.invalid = True
            ua_input.error_message = "Invalid user ID"
            ua_add_button.disabled = True
        else:
            ua_input.invalid = False
            ua_input.error_message = None
            ua_add_button.disabled = False
        
    async def onAddClick():
        try:
            await addTrackedUser(ua_input.value)
        except Exception as e:
            pass
        finally:
            ua_input.value = ""
            validateUserID(ua_input.value)  

    async def initializeTrackedUsers():
        for user_id in getUserActivitySettings("tracked_users"):
            try:
                user = await bot.fetch_user(int(user_id))
                ua_users_table.insert_rows([{
                    "id": user_id,
                    "cells": [
                        {"text": user.display_name, "imageUrl": user.display_avatar.url},
                        {"text": user_id},
                        {}
                    ]
                }])
            except discord.NotFound:
                continue

    ua_input.onInput = validateUserID
    ua_add_button.onClick = onAddClick

    bot.loop.create_task(initializeTrackedUsers())

    ua_tab.render()

userActivityTracker()

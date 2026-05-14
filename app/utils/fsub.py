from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.types import ChannelParticipant, ChannelParticipantAdmin, ChannelParticipantCreator
from telethon.errors import UserNotParticipantError
from app.database.connection import settings
import logging

logger = logging.getLogger(__name__)

async def is_user_fsubbed(client, user_id):
    if not settings.FORCE_SUB_CHANNELS:
        return True
        
    channels = settings.fsub_list
    for channel_id in channels:
        try:
            participant = await client(GetParticipantRequest(channel_id, user_id))
            if not isinstance(participant.participant, (ChannelParticipant, ChannelParticipantAdmin, ChannelParticipantCreator)):
                return False
        except UserNotParticipantError:
            return False
        except Exception as e:
            logger.error(f"Error checking fsub for {user_id} in {channel_id}: {e}")
            # If error (like bot not in channel), assume subscribed to avoid blocking users unnecessarily
            continue
            
    return True

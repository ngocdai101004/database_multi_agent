from datetime import datetime
from dbma.native.domain.enum.sender_type import SenderType

class Message:
    """
    Message of a ticket
    
    Args:
        id: ID of the message
        content: Content of the message
        created_by: ID of the user or agent who created the message
        sender_type: Type of the sender (USER or AGENT)
        created_at: Timestamp of the message
    """
    id: str
    content: str
    created_by: str
    sender_type: SenderType
    created_at: datetime
    
    def __init__(
        self,
        id: str,
        content: str,
        created_by: str,
        sender_type: SenderType,
        created_at: datetime
    ):
        self.id = id
        self.content = content
        self.created_by = created_by
        self.sender_type = sender_type
        self.created_at = created_at 
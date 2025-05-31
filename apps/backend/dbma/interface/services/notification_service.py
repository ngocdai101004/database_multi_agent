from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class NotificationService(ABC):
    """Interface for notification and alert services."""
    
    @abstractmethod
    async def send_notification(self, 
                              message: str, 
                              channels: List[str], 
                              metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Send notification to specified channels.
        
        Args:
            message: Notification message
            channels: List of target channels (e.g., ['slack', 'whatsapp'])
            metadata: Optional metadata for the notification
            
        Returns:
            bool indicating if notification was sent successfully
        """
        pass
    
    @abstractmethod
    async def send_alert(self, 
                        alert_type: str, 
                        message: str, 
                        severity: str,
                        metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Send alert to monitoring systems.
        
        Args:
            alert_type: Type of alert
            message: Alert message
            severity: Alert severity level
            metadata: Optional metadata for the alert
            
        Returns:
            bool indicating if alert was sent successfully
        """
        pass
    
    @abstractmethod
    async def get_notification_status(self, notification_id: str) -> Dict[str, Any]:
        """Get status of a sent notification.
        
        Args:
            notification_id: ID of the notification
            
        Returns:
            Dict containing notification status
        """
        pass
    
    @abstractmethod
    async def configure_channel(self, 
                              channel_type: str, 
                              config: Dict[str, Any]) -> bool:
        """Configure a notification channel.
        
        Args:
            channel_type: Type of channel to configure
            config: Channel configuration parameters
            
        Returns:
            bool indicating if configuration was successful
        """
        pass 
# /queue_tracker.py 
# (Backend Logic)
# The backend business logic that handles all the queue tracking functionality

import datetime

class QueueTracker:
    def __init__(self):
        self.is_active = False
        self.start_time = None
        self.initial_queue_size = 0
        self.current_queue_size = 0
        self.queue_history = []
        self.estimated_time_per_person = 60  # Default: 60 seconds per person
        self.finish_time = None
        
    def start_queue(self, queue_size):
        """Start a new queue with the given size"""
        self.is_active = True
        self.start_time = datetime.datetime.now()
        self.initial_queue_size = queue_size
        self.current_queue_size = queue_size
        self.queue_history = [(self.start_time, queue_size)]
        self.calculate_estimate()
        
    def update_queue(self, queue_size):
        """Update the queue with a new size and recalculate estimates"""
        if not self.is_active:
            return False
            
        now = datetime.datetime.now()
        # If the queue size hasn't changed, just log the time but don't recalculate
        if self.current_queue_size == queue_size:
            return True
            
        self.current_queue_size = queue_size
        self.queue_history.append((now, queue_size))
        
        # Recalculate time per person based on history
        if len(self.queue_history) >= 2:
            total_time = 0
            total_people = 0
            
            for i in range(1, len(self.queue_history)):
                prev_time, prev_size = self.queue_history[i-1]
                curr_time, curr_size = self.queue_history[i]
                
                time_diff = (curr_time - prev_time).total_seconds()
                people_diff = prev_size - curr_size
                
                # Only count positive differences (queue decreased)
                if people_diff > 0 and time_diff > 0:
                    total_time += time_diff
                    total_people += people_diff
            
            # Update the estimate only if we have meaningful data
            if total_people > 0 and total_time > 0:
                new_estimate = total_time / total_people
                # Apply some dampening to avoid wild swings in the estimate
                # 70% new estimate, 30% old estimate (if we had one before)
                if self.estimated_time_per_person > 0:
                    self.estimated_time_per_person = (0.7 * new_estimate) + (0.3 * self.estimated_time_per_person)
                else:
                    self.estimated_time_per_person = new_estimate
                
                # Ensure we never go below a reasonable minimum (10 seconds per person)
                if self.estimated_time_per_person < 10:
                    self.estimated_time_per_person = 10
        
        self.calculate_estimate()
        return True
        
    def calculate_estimate(self):
        """Calculate the estimated finish time based on current data"""
        if self.current_queue_size <= 0:
            self.finish_time = datetime.datetime.now()
            self.is_active = False
        else:
            # Make sure we have a positive value for time per person
            if self.estimated_time_per_person <= 0:
                self.estimated_time_per_person = 60  # Default fallback
                
            remaining_time = self.current_queue_size * self.estimated_time_per_person
            self.finish_time = datetime.datetime.now() + datetime.timedelta(seconds=remaining_time)
    
    def get_status(self):
        """Get the current status of the queue with all relevant time information"""
        if not self.is_active:
            if self.start_time is None:
                return {
                    "is_active": False,
                    "message": "No active queue"
                }
            else:
                return {
                    "is_active": False,
                    "message": "Queue complete",
                    "finish_time": self.finish_time.strftime("%I:%M %p")  # 12-hour format with AM/PM
                }
        
        now = datetime.datetime.now()
        
        # Calculate elapsed time
        elapsed = (now - self.start_time).total_seconds()
        
        # Calculate remaining time (ensure it's never negative)
        remaining = max(0, (self.finish_time - now).total_seconds())
        
        # Format time per person properly (it's in seconds, not a timestamp)
        time_per_person_formatted = self.format_time(self.estimated_time_per_person)
        
        return {
            "is_active": True,
            "current_size": self.current_queue_size,
            "initial_size": self.initial_queue_size,
            "start_time": self.start_time.strftime("%I:%M %p"),  # 12-hour format with AM/PM
            "current_time": now.strftime("%I:%M %p"),  # 12-hour format with AM/PM
            "elapsed_time": self.format_time(elapsed),
            "estimated_finish_time": self.finish_time.strftime("%I:%M %p"),  # 12-hour format with AM/PM
            "remaining_time": self.format_time(remaining),
            "estimated_time_per_person": time_per_person_formatted,
            "raw_seconds_per_person": round(self.estimated_time_per_person, 1)
        }
    
    @staticmethod
    def format_time(seconds):
        """Format seconds into HH:MM:SS format"""
        if seconds < 0:
            seconds = 0
        hours, remainder = divmod(int(seconds), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
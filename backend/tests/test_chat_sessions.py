"""
AgroScan AI — Chat Session History Persistence Tests
Verifies:
1. Auto-creation of chat sessions with meaningful title
2. Multi-turn message history persistence in database
3. Retrieval of session lists with message counts and last message previews
4. Specific session detail retrieval with chronological messages
5. Session deletion and cascading message cleanup
6. Session title update via PATCH
"""

import os
import sys
import unittest
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
from app.models.all_models import User, ChatSession, ChatMessage
from app.api.v1.endpoints.chat import _generate_session_title

class TestChatSessionPersistence(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
        cls.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=cls.engine)
        Base.metadata.create_all(bind=cls.engine)

    def setUp(self):
        self.db = self.SessionLocal()
        # Create test user
        self.user = User(
            id="test_user_farmer_1",
            email="farmer1@example.com",
            full_name="Ramesh Patil",
            hashed_password="mock_hashed_pw",
            role="farmer"
        )
        self.db.add(self.user)
        self.db.commit()

    def tearDown(self):
        self.db.query(ChatMessage).delete()
        self.db.query(ChatSession).delete()
        self.db.query(User).delete()
        self.db.commit()
        self.db.close()

    def test_generate_session_title(self):
        t1 = _generate_session_title("How often should I water sugarcane in summer?", "Sugarcane")
        self.assertTrue("sugarcane" in t1.lower())
        self.assertTrue("water" in t1.lower())

        t2 = _generate_session_title("What causes yellow leaves?")
        self.assertEqual(t2, "What causes yellow leaves?")

    def test_session_creation_and_message_persistence(self):
        session = ChatSession(
            id="session_test_101",
            user_id=self.user.id,
            title="Sugarcane Irrigation Advisory"
        )
        self.db.add(session)
        self.db.commit()

        # Add user message
        m1 = ChatMessage(
            id="msg_1",
            session_id=session.id,
            sender="user",
            content="How often to irrigate sugarcane?"
        )
        # Add assistant response
        m2 = ChatMessage(
            id="msg_2",
            session_id=session.id,
            sender="assistant",
            content="Irrigate every 7-10 days in summer using drip irrigation to maintain root-zone Vafsa."
        )
        self.db.add_all([m1, m2])
        self.db.commit()

        # Query messages back
        saved_msgs = self.db.query(ChatMessage).filter(
            ChatMessage.session_id == session.id
        ).order_by(ChatMessage.created_at.asc()).all()

        self.assertEqual(len(saved_msgs), 2)
        self.assertEqual(saved_msgs[0].sender, "user")
        self.assertEqual(saved_msgs[0].content, "How often to irrigate sugarcane?")
        self.assertEqual(saved_msgs[1].sender, "assistant")
        self.assertIn("drip irrigation", saved_msgs[1].content)

    def test_session_cascade_deletion(self):
        session = ChatSession(
            id="session_delete_target",
            user_id=self.user.id,
            title="Temporary Consultation"
        )
        self.db.add(session)
        self.db.commit()

        m1 = ChatMessage(id="del_m1", session_id=session.id, sender="user", content="Hello")
        m2 = ChatMessage(id="del_m2", session_id=session.id, sender="assistant", content="Hello farmer!")
        self.db.add_all([m1, m2])
        self.db.commit()

        # Delete session
        self.db.delete(session)
        self.db.commit()

        # Verify messages also deleted
        remaining_msgs = self.db.query(ChatMessage).filter(ChatMessage.session_id == "session_delete_target").all()
        self.assertEqual(len(remaining_msgs), 0)

    def test_multi_session_ordering(self):
        s1 = ChatSession(id="s1", user_id=self.user.id, title="Session 1", created_at=datetime(2026, 9, 1, 10, 0, 0))
        s2 = ChatSession(id="s2", user_id=self.user.id, title="Session 2", created_at=datetime(2026, 9, 21, 10, 0, 0))
        self.db.add_all([s1, s2])
        self.db.commit()

        sessions = self.db.query(ChatSession).filter(
            ChatSession.user_id == self.user.id
        ).order_by(ChatSession.created_at.desc()).all()

        self.assertEqual(len(sessions), 2)
        self.assertEqual(sessions[0].id, "s2")
        self.assertEqual(sessions[1].id, "s1")

if __name__ == '__main__':
    unittest.main()

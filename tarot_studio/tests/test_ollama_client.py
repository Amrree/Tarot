"""
Tests for the Ollama client.
"""

import pytest
import asyncio
import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tarot_studio.ai.ollama_client import OllamaClient, ConversationContext

class TestOllamaClient:
    """Test cases for the Ollama client."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.client = OllamaClient()
    
    @pytest.mark.asyncio
    async def test_client_initialization(self):
        """Test that the client initializes correctly."""
        assert self.client.model_name == "llama3.2"
        assert self.client.base_url == "http://localhost:11434"
        assert self.client.client is not None
    
    @pytest.mark.asyncio
    async def test_check_connection_success(self):
        """Test successful connection check."""
        with patch.object(self.client.client, 'list') as mock_list:
            mock_list.return_value = {'models': []}
            
            connected = await self.client.check_connection()
            assert connected is True
    
    @pytest.mark.asyncio
    async def test_check_connection_failure(self):
        """Test failed connection check."""
        with patch.object(self.client.client, 'list') as mock_list:
            mock_list.side_effect = Exception("Connection failed")
            
            connected = await self.client.check_connection()
            assert connected is False
    
    @pytest.mark.asyncio
    async def test_pull_model_success(self):
        """Test successful model pull."""
        with patch.object(self.client.client, 'pull') as mock_pull:
            mock_pull.return_value = None
            
            success = await self.client.pull_model("test-model")
            assert success is True
    
    @pytest.mark.asyncio
    async def test_pull_model_failure(self):
        """Test failed model pull."""
        with patch.object(self.client.client, 'pull') as mock_pull:
            mock_pull.side_effect = Exception("Pull failed")
            
            success = await self.client.pull_model("test-model")
            assert success is False
    
    def test_build_reading_prompt(self):
        """Test reading prompt building."""
        spread_data = {
            'reading_id': 'test_reading_001',
            'spread_name': 'Three Card Spread',
            'cards': [
                {
                    'position': 'past',
                    'card': 'The Sun (upright)',
                    'orientation': 'upright',
                    'meaning': 'Joy, success, and vitality'
                }
            ]
        }
        
        prompt = self.client._build_reading_prompt(spread_data, None)
        
        assert 'test_reading_001' in prompt
        assert 'Three Card Spread' in prompt
        assert 'The Sun' in prompt
        assert 'JSON' in prompt
        assert 'reading_id' in prompt
        assert 'cards' in prompt
        assert 'summary' in prompt
        assert 'advice' in prompt
    
    def test_build_card_chat_prompt(self):
        """Test card chat prompt building."""
        card_data = {
            'name': 'The Sun',
            'orientation': 'upright',
            'meaning': 'Joy, success, and vitality',
            'position': 'present'
        }
        
        user_message = "What does this card mean for my career?"
        
        prompt = self.client._build_card_chat_prompt(card_data, user_message, None)
        
        assert 'The Sun' in prompt
        assert 'upright' in prompt
        assert 'Joy, success, and vitality' in prompt
        assert 'present' in prompt
        assert 'What does this card mean for my career?' in prompt
    
    def test_build_reading_chat_prompt(self):
        """Test reading chat prompt building."""
        reading_data = {
            'title': 'Career Reading',
            'spread_name': 'Three Card Spread',
            'cards': [
                {'name': 'The Sun', 'orientation': 'upright'}
            ]
        }
        
        user_message = "What should I focus on?"
        
        prompt = self.client._build_reading_chat_prompt(reading_data, user_message, None)
        
        assert 'Career Reading' in prompt
        assert 'Three Card Spread' in prompt
        assert 'The Sun' in prompt
        assert 'What should I focus on?' in prompt
    
    def test_parse_json_response_valid(self):
        """Test parsing valid JSON response."""
        response_text = '{"summary": "Test summary", "advice": ["Test advice"]}'
        
        result = self.client._parse_json_response(response_text)
        
        assert result['summary'] == "Test summary"
        assert result['advice'] == ["Test advice"]
    
    def test_parse_json_response_invalid(self):
        """Test parsing invalid JSON response."""
        response_text = "This is not JSON"
        
        result = self.client._parse_json_response(response_text)
        
        assert 'summary' in result
        assert 'advice' in result
        assert 'I\'m having trouble processing' in result['summary']
    
    def test_parse_json_response_with_text(self):
        """Test parsing JSON response with surrounding text."""
        response_text = 'Here is the response: {"summary": "Test summary"} End of response'
        
        result = self.client._parse_json_response(response_text)
        
        assert result['summary'] == "Test summary"
    
    def test_create_error_response(self):
        """Test creating error response."""
        response = self.client._create_error_response("test_reading")
        
        assert response.reading_id == "test_reading"
        assert "trouble generating" in response.summary
        assert len(response.advice) > 0
        assert len(response.follow_up_questions) > 0
    
    def test_create_fallback_response(self):
        """Test creating fallback response."""
        response = self.client._create_fallback_response()
        
        assert 'summary' in response
        assert 'advice' in response
        assert 'follow_up_questions' in response
        assert 'trouble processing' in response['summary']
    
    @pytest.mark.asyncio
    async def test_generate_reading_interpretation_success(self):
        """Test successful reading interpretation generation."""
        spread_data = {
            'reading_id': 'test_reading_001',
            'spread_name': 'Three Card Spread',
            'cards': [
                {
                    'position': 'past',
                    'card': 'The Sun (upright)',
                    'orientation': 'upright',
                    'meaning': 'Joy, success, and vitality'
                }
            ]
        }
        
        mock_response = {
            'response': '{"summary": "Test summary", "advice": ["Test advice"], "follow_up_questions": ["Test question"]}'
        }
        
        with patch.object(self.client.client, 'generate', return_value=mock_response):
            response = await self.client.generate_reading_interpretation(spread_data)
            
            assert response.reading_id == 'test_reading_001'
            assert response.summary == "Test summary"
            assert response.advice == ["Test advice"]
            assert response.follow_up_questions == ["Test question"]
    
    @pytest.mark.asyncio
    async def test_generate_reading_interpretation_failure(self):
        """Test failed reading interpretation generation."""
        spread_data = {
            'reading_id': 'test_reading_001',
            'spread_name': 'Three Card Spread',
            'cards': []
        }
        
        with patch.object(self.client.client, 'generate', side_effect=Exception("Generation failed")):
            response = await self.client.generate_reading_interpretation(spread_data)
            
            assert response.reading_id == 'test_reading_001'
            assert "trouble generating" in response.summary
            assert len(response.advice) > 0
    
    @pytest.mark.asyncio
    async def test_chat_with_card_success(self):
        """Test successful card chat."""
        card_data = {
            'name': 'The Sun',
            'orientation': 'upright',
            'meaning': 'Joy, success, and vitality',
            'position': 'present'
        }
        
        user_message = "What does this card mean?"
        
        mock_response = {'response': 'This card represents joy and success in your life.'}
        
        with patch.object(self.client.client, 'generate', return_value=mock_response):
            response = await self.client.chat_with_card(card_data, user_message)
            
            assert "joy and success" in response
    
    @pytest.mark.asyncio
    async def test_chat_with_card_failure(self):
        """Test failed card chat."""
        card_data = {'name': 'The Sun'}
        user_message = "What does this card mean?"
        
        with patch.object(self.client.client, 'generate', side_effect=Exception("Chat failed")):
            response = await self.client.chat_with_card(card_data, user_message)
            
            assert "trouble connecting" in response
    
    @pytest.mark.asyncio
    async def test_chat_with_reading_success(self):
        """Test successful reading chat."""
        reading_data = {
            'title': 'Career Reading',
            'spread_name': 'Three Card Spread',
            'cards': [{'name': 'The Sun'}]
        }
        
        user_message = "What should I focus on?"
        
        mock_response = {'response': 'Focus on your goals and take action.'}
        
        with patch.object(self.client.client, 'generate', return_value=mock_response):
            response = await self.client.chat_with_reading(reading_data, user_message)
            
            assert "Focus on your goals" in response
    
    @pytest.mark.asyncio
    async def test_chat_with_reading_failure(self):
        """Test failed reading chat."""
        reading_data = {'title': 'Career Reading'}
        user_message = "What should I focus on?"
        
        with patch.object(self.client.client, 'generate', side_effect=Exception("Chat failed")):
            response = await self.client.chat_with_reading(reading_data, user_message)
            
            assert "trouble connecting" in response
    
    @pytest.mark.asyncio
    async def test_stream_response(self):
        """Test streaming response."""
        mock_stream = [
            {'response': 'Hello'},
            {'response': ' world'},
            {'response': '!'}
        ]
        
        with patch.object(self.client.client, 'generate', return_value=mock_stream):
            responses = []
            async for chunk in self.client.stream_response("Test prompt"):
                responses.append(chunk)
            
            assert len(responses) == 3
            assert responses[0] == 'Hello'
            assert responses[1] == ' world'
            assert responses[2] == '!'
    
    @pytest.mark.asyncio
    async def test_stream_response_failure(self):
        """Test streaming response failure."""
        with patch.object(self.client.client, 'generate', side_effect=Exception("Stream failed")):
            responses = []
            async for chunk in self.client.stream_response("Test prompt"):
                responses.append(chunk)
            
            assert len(responses) == 1
            assert "Error: Unable to generate response" in responses[0]

if __name__ == "__main__":
    pytest.main([__file__])
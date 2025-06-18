from openai import OpenAI
import os
import json
from typing import List, Dict, Any
from fastapi import HTTPException

class OpenAIService:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        self.client = OpenAI(api_key=api_key)

    def get_job_description_function(self) -> Dict[str, Any]:
        """Define the function schema for job description generation"""
        return {
            "name": "generate_job_description",
            "description": "Generate a comprehensive job description based on job details and required tools",
            "parameters": {
                "type": "object",
                "properties": {
                    "description": {
                        "type": "string",
                        "description": "A comprehensive job description including responsibilities, requirements, benefits, and required tools"
                    }
                },
                "required": ["description"]
            }
        }

    def generate_job_description(self, job_data: Dict[str, Any], required_tools: List[str]) -> str:
        """Generate job description using OpenAI GPT-4 with streaming and function calling"""
        try:
            # Prepare the prompt with required tools
            tools_text = ", ".join(required_tools) if required_tools else "Not specified"
            
            prompt = f"""
            Generate a comprehensive job description for the following position:
            
            Title: {job_data['title']}
            Company: {job_data['company']}
            Location: {job_data['location']}
            Salary Range: {job_data.get('salary_range', 'Not specified')}
            Required Tools: {tools_text}
            
            Please include:
            1. Job overview and company introduction
            2. Key responsibilities and duties
            3. Required qualifications and experience
            4. Preferred qualifications
            5. Required tools and technologies: {tools_text}
            6. Benefits and perks
            7. Company culture and work environment
            8. Growth opportunities
            
            Make the description compelling and professional.
            """
            
            # Call OpenAI API with function calling and streaming
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional HR specialist who creates compelling and comprehensive job descriptions. Focus on making the role attractive to qualified candidates."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                functions=[self.get_job_description_function()],
                function_call={"name": "generate_job_description"},
                stream=True
            )
            
            # Process streaming response
            full_description = ""
            for chunk in response:
                if chunk.choices[0].delta.function_call:
                    function_call = chunk.choices[0].delta.function_call
                    if function_call.arguments:
                        full_description += function_call.arguments
            
            # Parse the function call arguments
            try:
                description_data = json.loads(full_description)
                generated_description = description_data.get("description", "")
            except json.JSONDecodeError as e:
                # Fallback: use the raw response
                generated_description = full_description
                print(f"Warning: JSON parsing failed, using raw response: {e}")
            
            if not generated_description.strip():
                raise ValueError("Generated description is empty")
            
            return generated_description
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error generating job description: {str(e)}"
            ) 
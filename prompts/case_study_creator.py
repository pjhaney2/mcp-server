def get_case_study_prompt(client_name: str = "the client", focus_area: str = "general") -> str:
    """
    Creates a prompt for generating a one-page case study from reports or documents.
    
    Args:
        document_type: Type of document provided (e.g., "final report", "project summary", "research findings")
        client_name: Name of the client or organization (defaults to "the client")
        focus_area: Specific area to focus on (e.g., "economic development", "housing", "demographics")
    
    Returns:
        A formatted prompt string for case study generation
    """
    template = """Create a concise one-page case study from the provided document(s). The case study should be professional, engaging, and follow this exact structure:

**Structure Requirements:**
1. First Half: Challenge/Context section
   - Header: A compelling title that captures the core challenge or context
   - Body: 1-2 paragraphs explaining the situation, problem, or context that led to this work

2. Second Half: Solution/Action section  
   - Header: A clear title that summarizes the solution or action taken
   - Body: 1-2 paragraphs describing what was done, methodologies used, and outcomes achieved

**Content Guidelines:**
- Client: {client_name}
- Focus Area: {focus_area}
- Total length: Slightly less than one page (300-400 words)
- Tone: Professional yet accessible
- Include specific data points and outcomes where available
- Highlight the value delivered and impact achieved
- Always be sure the tone of the case study reflects positively upon the client

**Formatting:**
- Use clear, descriptive headers
- Keep paragraphs concise and impactful
- Emphasize key metrics or results
- Ensure smooth flow between challenge and solution sections

Please analyze the provided document and create a compelling case study that tells the story of the challenge faced and the solution delivered."""
    
    return template.format(
        client_name=client_name,
        focus_area=focus_area
    )
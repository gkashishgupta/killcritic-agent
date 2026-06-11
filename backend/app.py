from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
import re

app = Flask(__name__)
CORS(app)

# Try to import OpenAI
try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

def calculate_dynamic_score(idea):
    """
    Calculate a dynamic score based on idea quality metrics
    """
    score = 5.0  # Base score
    
    # Length analysis (idea substance)
    if len(idea) < 50:
        score -= 2.0  # Too vague
    elif len(idea) < 100:
        score -= 0.5
    elif len(idea) > 500:
        score += 0.5  # Detailed thinking
    
    # Keywords indicating strong ideas
    strong_keywords = ['problem', 'solution', 'market', 'user', 'revenue', 'differentiation', 'target', 'validation']
    keyword_count = sum(1 for keyword in strong_keywords if keyword.lower() in idea.lower())
    score += (keyword_count * 0.3)
    
    # Clarity indicators
    has_numbers = bool(re.search(r'\d+[%\$K]', idea))
    if has_numbers:
        score += 0.5
    
    # Market understanding
    market_keywords = ['market size', 'tam', 'customers', 'competition', 'moat', 'competitive advantage']
    market_score = sum(1 for kw in market_keywords if kw.lower() in idea.lower())
    score += (market_score * 0.4)
    
    # Business model clarity
    model_keywords = ['subscription', 'freemium', 'one-time', 'marketplace', 'b2b', 'b2c', 'revenue model']
    model_score = sum(1 for kw in model_keywords if kw.lower() in idea.lower())
    score += (model_score * 0.3)
    
    # Red flags (decrease score)
    red_flags = ['hope', 'eventually', 'maybe', 'possibly', 'might work', 'unproven', 'untested']
    red_flag_count = sum(1 for flag in red_flags if flag.lower() in idea.lower())
    score -= (red_flag_count * 0.5)
    
    # Cap score between 4 and 9
    score = max(4.0, min(9.0, score))
    
    return round(score, 1)

def analyze_idea_with_ai(idea, use_example=False):
    """
    Analyze startup idea using OpenAI API with brutal honesty
    """
    if not HAS_OPENAI:
        return analyze_idea_fallback(idea, use_example=use_example)
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        return analyze_idea_fallback(idea, use_example=use_example)
    
    try:
        client = OpenAI(api_key=api_key)
        
        prompt = f"""You are a brutally honest, no-nonsense venture capitalist and startup advisor. Your job is to tear apart mediocre ideas and provide constructive feedback on viable ones. Be savage but professional. No sugar-coating.

Analyze this startup idea with brutal honesty:
{idea}

IMPORTANT: Respond ONLY with valid JSON, no markdown, no explanations, no preamble:
{{
    "summary": "A brutally honest 2-3 sentence summary. Don't hold back - if it's weak, say so directly.",
    "clarity_score": 8,
    "opportunity_score": 6,
    "competitive_score": 4,
    "execution_score": 7,
    "overall_clarity": "Is the problem clearly articulated? Rate the founder's ability to communicate. Be harsh if they're vague.",
    "opportunity_analysis": "Is there ACTUALLY a market? Be brutally honest about TAM, growth potential, and whether this is solving a real problem or a nice-to-have.",
    "competitive_landscape": "Who are the real competitors? Don't let them hide behind 'there's no direct competitor' - brutal truth about what they're actually competing against.",
    "strengths": [
        "Real, defensible advantage 1",
        "Real, defensible advantage 2",
        "Real, defensible advantage 3"
    ],
    "fatal_flaws": [
        "Critical flaw that could kill this 1",
        "Critical flaw that could kill this 2",
        "Critical flaw that could kill this 3"
    ],
    "risks": [
        "Major execution risk",
        "Major market risk",
        "Major competitive risk",
        "Major regulatory/technical risk"
    ],
    "improvement_suggestions": [
        "What they MUST do to be fundable",
        "What they MUST do to be fundable",
        "What they MUST do to be fundable"
    ],
    "mvp_roadmap": [
        "Phase 1 (weeks 0-4): Minimum viable proof of concept",
        "Phase 2 (weeks 4-12): Initial user validation and iteration",
        "Phase 3 (weeks 12+): Product-market fit validation"
    ],
    "verdict": "PASS/FAIL/MAYBE - Be direct. Would you fund this? Why or why not?",
    "score": 5.5,
    "failure_probability": "very-high/high/medium/medium-low/low"
}}"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a brutally honest VC advisor. You respond ONLY with valid JSON. No markdown, no code blocks, no explanations. Just pure JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=2000
        )
        
        # Parse the response
        content = response.choices[0].message.content.strip()
        
        # Try to extract JSON from the response
        try:
            analysis = json.loads(content)
        except json.JSONDecodeError:
            # If JSON parsing fails, try to extract JSON from the content
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                try:
                    analysis = json.loads(json_match.group())
                except:
                    return analyze_idea_fallback(idea)
            else:
                return analyze_idea_fallback(idea)
        
        # Always ensure the final score is based on the submitted idea
        analysis['score'] = calculate_dynamic_score(idea)

        if use_example:
            analysis['score'] = max(4.0, min(9.0, analysis['score'] + 1.0))
            strengths = analysis.get('strengths', [])
            strengths.extend([
                '✓ Example idea is polished with clear positioning.',
                '✓ Strong structure with market, solution, and revenue clarity.',
                '✓ High-readiness concept for quick validation.'
            ])
            analysis['strengths'] = list(dict.fromkeys(strengths))
            if 'fatal_flaws' in analysis and isinstance(analysis['fatal_flaws'], list):
                analysis['fatal_flaws'] = analysis['fatal_flaws'][:2]

        return analysis
    
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return analyze_idea_fallback(idea)

def analyze_idea_fallback(idea, use_example=False):
    """
    Fallback analysis with brutal honesty - no sugar coating
    """
    idea_lower = idea.lower()
    
    # Calculate dynamic score
    base_score = calculate_dynamic_score(idea)
    
    # Detect keywords for contextual analysis
    has_problem = any(word in idea_lower for word in ['problem', 'pain point', 'issue', 'frustration'])
    has_market_size = any(word in idea_lower for word in ['market', 'customers', 'users', 'tam', 'b2b', 'b2c'])
    has_solution = any(word in idea_lower for word in ['solution', 'platform', 'app', 'service', 'tool'])
    has_differentiation = any(word in idea_lower for word in ['differentiation', 'unique', 'moat', 'competitive advantage', 'defensible'])
    has_revenue = any(word in idea_lower for word in ['subscription', 'freemium', 'pricing', 'revenue', 'monetization', 'payment'])
    has_validation = any(word in idea_lower for word in ['validated', 'proven', 'data', 'research', 'survey', 'evidence'])
    
    # Brutal assessment
    if len(idea) < 50:
        summary = f"This is too vague. {base_score}/10 at best. You haven't articulated a clear problem or solution. Come back with a fully formed idea."
        clarity_verdict = "FAIL"
    elif not has_problem:
        summary = f"You're describing a solution, not a problem. Where's the actual pain point? {base_score}/10 - Show your work."
        clarity_verdict = "FAIL"
    elif not has_market_size:
        summary = f"No clear market definition. Are you solving for 100 people or 100 million? {base_score}/10 - This is critical."
        clarity_verdict = "MAYBE"
    elif not has_solution and not has_differentiation:
        summary = f"Another 'me too' idea without a real moat. {base_score}/10 - Why should anyone pick you over what exists?"
        clarity_verdict = "FAIL"
    elif has_validation:
        summary = f"You've done your homework. {base_score}/10 - You have real insight. Now scale it."
        clarity_verdict = "PASS"
    else:
        summary = f"Decent idea, but unproven. {base_score}/10 - Ideas are cheap. Show traction."
        clarity_verdict = "MAYBE"
    
    # Strengths - only if they exist
    strengths = []
    if has_problem:
        strengths.append("✓ Problem-focused thinking (rare for founders)")
    if has_market_size:
        strengths.append("✓ Market awareness")
    if has_solution:
        strengths.append("✓ Has a proposed solution")
    if has_differentiation:
        strengths.append("✓ Awareness of competitive landscape")
    
    if not strengths:
        strengths = ["Honestly? You're early. Find ONE real strength and build on it."]
    
    # Fatal Flaws - be harsh
    fatal_flaws = []
    if not has_problem:
        fatal_flaws.append("❌ No clear problem statement - you're solving for ghosts")
    if not has_market_size:
        fatal_flaws.append("❌ TAM undefined - you don't know your addressable market")
    if not has_differentiation:
        fatal_flaws.append("❌ Zero competitive differentiation - you're a feature, not a company")
    if not has_revenue:
        fatal_flaws.append("❌ No revenue model defined - can you actually make money?")
    if not has_validation:
        fatal_flaws.append("❌ Entirely unvalidated - have you talked to a single customer?")
    
    if len(fatal_flaws) > 3:
        fatal_flaws = fatal_flaws[:3]
    elif not fatal_flaws:
        fatal_flaws = ["None identified yet, but you need to prove this in market"]

    if use_example:
        strengths.extend([
            '✓ Example idea has a clean, investor-friendly structure.',
            '✓ Contains clear target audience and value proposition.',
            '✓ Feels polished and ready for rapid pitch testing.'
        ])
        strengths = list(dict.fromkeys(strengths))
        base_score = max(4.0, min(9.0, base_score + 1.0))
        fatal_flaws = fatal_flaws[:2]

    return {
        "summary": summary,
        "clarity_score": min(8, base_score + 1) if has_problem else max(1, base_score - 1),
        "opportunity_score": max(1, base_score + 0.5) if has_market_size else max(1, base_score - 1),
        "competitive_score": max(1, base_score) if has_differentiation else max(1, base_score - 1.5),
        "execution_score": max(1, base_score - 0.5),
        
        "overall_clarity": "HARSH TRUTH: " + (
            "Clear and focused. You know what you're solving." if has_problem and has_market_size
            else "Vague. You're describing a feature, not a company." if not has_problem
            else "Unclear. You need to narrow your focus."
        ),
        
        "opportunity_analysis": "MARKET REALITY: " + (
            f"Real market opportunity identified. TAM is substantial. You're in a growing space." if has_market_size
            else f"You haven't defined your market. This is a showstopper. How many potential customers? What's your TAM?"
        ),
        
        "competitive_landscape": "COMPETITIVE TRUTH: " + (
            f"You understand the competitive dynamics. There's a defensible position here." if has_differentiation
            else f"You're blind to competition. Even if there's no direct competitor, you're competing against status quo and existing alternatives."
        ),
        
        "strengths": strengths,
        
        "fatal_flaws": fatal_flaws,
        
        "risks": [
            "🔴 Market timing and adoption risk - will customers actually switch?",
            "🔴 Execution complexity - do you have the team to build this?",
            "🔴 Competitive response - big players will copy if this works",
            "🔴 Unit economics - will you make money at scale?"
        ],
        
        "improvement_suggestions": [
            "1. PROVE THE PROBLEM: Get 50+ customer interviews. Document the pain.",
            "2. BUILD THE MVP: Stop talking, start building. Show a working prototype.",
            "3. VALIDATE BUSINESS MODEL: Show unit economics. Prove willingness to pay."
        ],
        
        "mvp_roadmap": [
            "Phase 1 (Weeks 1-4): Build MVP. Get it in front of 20 users. Don't overcomplicate it.",
            "Phase 2 (Weeks 5-12): Iterate based on feedback. Find product-market fit signals.",
            "Phase 3 (Week 13+): Scale what works. Double down on retention and growth metrics."
        ],
        
        "verdict": f"{clarity_verdict} - {'This could work if you execute.' if clarity_verdict == 'MAYBE' else 'Get back to us when you have proof.' if clarity_verdict == 'FAIL' else 'This is fundable. Let us talk.'}",
        
        "score": base_score,
        
        "failure_probability": (
            "very-high" if base_score < 3
            else "high" if base_score < 4.5
            else "medium" if base_score < 6.5
            else "medium-low" if base_score < 8
            else "low"
        )
    }

@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Main API endpoint for startup idea analysis
    """
    try:
        data = request.get_json()
        
        if not data or 'idea' not in data:
            return jsonify({
                "error": "Missing 'idea' field in request"
            }), 400
        
        idea = data.get('idea', '').strip()
        use_example = bool(data.get('use_example', False))
        
        if not idea or len(idea) < 10:
            return jsonify({
                "error": "Idea must be at least 10 characters long. Give us something to work with."
            }), 400
        
        # Get analysis
        analysis = analyze_idea_with_ai(idea, use_example=use_example)
        
        return jsonify({
            "agent": "KILLCRITIC",
            "analysis": analysis,
            "ai_model": "gpt-3.5-turbo (Brutal Mode)" if HAS_OPENAI and os.getenv('OPENAI_API_KEY') else "fallback (Brutal Mode)",
            "mode": "BRUTAL HONESTY"
        })
    
    except Exception as e:
        print(f"Error in /analyze endpoint: {e}")
        return jsonify({
            "error": f"Internal server error: {str(e)}"
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """
    Health check endpoint
    """
    return jsonify({
        "status": "ok",
        "ai_available": HAS_OPENAI and bool(os.getenv('OPENAI_API_KEY')),
        "mode": "BRUTAL AI MODE" if (HAS_OPENAI and os.getenv('OPENAI_API_KEY')) else "BRUTAL FALLBACK MODE",
        "message": "Ready to tear apart your startup idea with honesty"
    })

if __name__ == '__main__':
    print("🚀 KILLCRITIC Backend Starting...")
    print("💀 Mode: BRUTAL HONESTY - No sugar coating")
    print(f"📊 AI Mode: {'ENABLED (GPT-3.5 Turbo - Savage Mode)' if HAS_OPENAI and os.getenv('OPENAI_API_KEY') else 'FALLBACK (Still Brutal)'}")
    if not os.getenv('OPENAI_API_KEY'):
        print("💡 Tip: Set OPENAI_API_KEY environment variable for AI-powered savage analysis")
    print("⚠️  WARNING: This system does not hold back. Prepare for honest feedback.\n")
    app.run(debug=True, port=5000)
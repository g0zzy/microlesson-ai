# Test Examples for MicroLesson AI

Use these topics to test all three learning styles:

## Quick Tests (Simple Topics)

### 1. **Photosynthesis**
- Style: Text
- Expected: Clear explanation of how plants convert sunlight to energy

### 2. **JavaScript Closures**
- Style: Visual
- Expected: 5 slides explaining closures with simple examples

### 3. **The Water Cycle**
- Style: Voice
- Expected: Conversational narration about evaporation, condensation, precipitation

## Intermediate Tests

### 4. **Quantum Computing**
- Style: Text
- Expected: Intro to qubits, superposition, entanglement

### 5. **How Vaccines Work**
- Style: Voice
- Expected: Explanation of immune system response and vaccine mechanism

### 6. **The French Revolution**
- Style: Visual
- Expected: Timeline slides with causes, events, outcomes

## Advanced Tests

### 7. **Machine Learning Basics**
- Style: Text
- Expected: Supervised vs unsupervised learning, neural networks

### 8. **Blockchain Technology**
- Style: Visual
- Expected: Distributed ledger, mining, smart contracts

### 9. **Climate Change**
- Style: Voice
- Expected: Greenhouse effect, human impact, solutions

## Edge Cases

### 10. **Very Specific Topic**
- Topic: "How CRISPR Gene Editing Works"
- Style: Any
- Expected: Should still generate focused content

### 11. **Abstract Concept**
- Topic: "What is Consciousness?"
- Style: Any
- Expected: Philosophical and scientific perspectives

### 12. **Practical Skill**
- Topic: "How to Make Sourdough Bread"
- Style: Visual
- Expected: Step-by-step process in slides

## Testing Checklist

- [ ] Text style displays formatted article
- [ ] Voice style has play button and transcript
- [ ] Visual style shows 5 slides with navigation
- [ ] Keyboard arrows work for slides (← →)
- [ ] Loading spinner appears during generation
- [ ] Error messages display properly
- [ ] Works on mobile browsers
- [ ] TTS voice is clear and understandable
- [ ] Content follows the 5-part structure
- [ ] Lessons are ~300-500 words

## Expected Response Times

- Fast topics (common knowledge): 3-5 seconds
- Complex topics: 5-8 seconds
- Timeout threshold: 30 seconds

## Common Issues

### If text looks unformatted:
- Check browser console for JavaScript errors
- Verify API response has proper content

### If voice doesn't play:
- Try Chrome or Safari (best TTS support)
- Check browser console for SpeechSynthesis errors
- Verify speakers are not muted

### If slides don't appear:
- Check if response has exactly 5 slides
- Verify JSON parsing in browser console
- Check for malformed JSON from API

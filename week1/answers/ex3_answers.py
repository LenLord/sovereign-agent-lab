"""
Exercise 3 — Answers
====================
Fill this in after completing the three Rasa conversations.

CALM vs Old Rasa — what changed
---------------------------------
The old open-source Rasa approach used:
  - nlu.yml: intent training examples
  - rules.yml: explicit dialogue rules
  - FormValidationAction: Python class to parse slot values

Rasa Pro CALM uses:
  - flows.yml: natural language descriptions of what each flow does
  - from_llm slots: the LLM extracts values from conversation
  - ONE custom action: ActionValidateBooking for the business rules

The conversation is the same from the manager's perspective.
The machinery underneath is completely different.

CONVERSATION SCRIPTS
---------------------
Conversation 1 (happy path):
  You:    calling to confirm a booking
  Agent:  [asks guest count]
  You:    160 guests
  Agent:  [asks vegan count]
  You:    about 50 need vegan
  Agent:  [asks deposit]
  You:    £200 deposit
  Agent:  [confirms or escalates?]

Conversation 2 (deposit too high):
  Same as above but use a deposit above £300 (e.g. "£500 deposit").

Conversation 3 (out of scope):
  Start normally, then when asked for vegan count say something like
  "can you arrange parking for the speakers?" and observe what happens.
  Does CALM handle this differently than the old rules approach?
"""

# ── Conversation 1: Happy path ─────────────────────────────────────────────

CONVERSATION_1_TRACE = """
Bot loaded. Type a message and press enter (use '/stop' to exit): 
Your input ->  calling to confirm a booking                        
How many guests are you confirming for tonight's event?
Your input ->  160 guests                                          
And how many of those guests will need vegan meals?
Your input ->  about 50 need vegan                                 
2026-04-13 19:16:14 WARNING  rasa.utils.log_utils  - [warning  ] CompactLLMCommandGenerator.parse_commands actions='<think>
Okay, let\'s see. The user said, "about 50 need vegan." The current flow is confirm_booking, and the current step is asking for vegan_count. The guest_count is already set to 160. So the user is providing the number of vegan guests here.                               
                                                                   
First, I need to set the vegan_count slot. The user mentioned "about 50," so I should take that as the value. The slot expects a float, so even though it\'s "about," I should just use 50.0. So the action would be set slot vegan_count 50.0.                             
                                                                   
Next, I need to check if there are other slots that need to be filled. The remaining slot in the confirm_booking flow is deposit_amount_gbp, which is still undefined. Since the user hasn\'t mentioned the deposit yet, the next step should be to ask for that. But the task here is only to respond to the last message, which is providing the vegan count. So maybe after setting the slot, the AI would proceed to the next step in the flow, which is requesting the deposit amount. Wait, but the instructions say to focus on the last message and take it one step at a time. So maybe after setting the vegan_count, the next action is to ask for the deposit. But the example in the slot extraction shows that when a value is provided, you set the slot and start the flow if needed. However, in this case, the flow is already active. So the correct action here is to set the slot and then proceed to the next step in the flow. But according to the available actions, after setting the slot, if the flow requires more steps, the AI should continue. But the user\'s last message only addresses the vegan_count. So the action list should include setting the slot and then starting the next step, which would be asking for deposit_amount_gbp. Wait, but the current step\'s requested slot is vegan_count, which is now filled. So the next step in the flow would be to ask for deposit_amount_gbp. However, the task is to output actions based on the user\'s last message. Since the user provided the vegan_count, the AI should set that slot and then move to the next step in the flow, which is to ask for the deposit. But according to the instructions, the action list should be in response to the user\'s last message. So the correct actions here are to set the vegan_count slot and then start the next' message='No commands were parsed from the LLM actions.'                                 
2026-04-13 19:16:14 WARNING  rasa.utils.log_utils  - [warning  ] llm_command_generator.predict_commands message='No commands were predicted as the LLM response could not be parsed or the LLM responded with an invalid command. Returning a CannotHandleCommand instead.' 
I’m sorry I am unable to understand you, could you please rephrase?
And how many of those guests will need vegan meals?
Your input ->  about 50 need vegan                                 
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  £200 deposit                                        
Thank you — booking confirmed. 160 guests, 50 requiring vegan meals, £200 deposit accepted. I'll send written confirmation to the organiser shortly.                                                     
Is there anything else I can help you with?
"""

CONVERSATION_1_OUTCOME = "confirmed"   # "confirmed" or "escalated"

# ── Conversation 2: Deposit too high ───────────────────────────────────────

CONVERSATION_2_TRACE = """
Bot loaded. Type a message and press enter (use '/stop' to exit): 
Your input ->  calling to confirm a booking        
How many guests are you confirming for tonight's event?
Your input ->  160 guests  
And how many of those guests will need vegan meals?
Your input ->  about 50 need vegan   
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  £500 deposit  
I need to check one thing with the organiser before I can confirm. The issue is: a deposit of £500 exceeds the organiser's authorised limit of £300. Can I call you back within 15 minutes?              
Is there anything else I can help you with?
"""

CONVERSATION_2_OUTCOME = "escalated"   # "confirmed" or "escalated"
CONVERSATION_2_REASON  = "Because the deposit suggested was higher than a limit of £300. So Guard 2: Deposit authorisation limit worked and escalated this"   # the reason the agent gave for escalating

# ── Conversation 3: Out of scope ───────────────────────────────────────────

CONVERSATION_3_TRACE = """
Bot loaded. Type a message and press enter (use '/stop' to exit): 
Your input ->  calling to confirm a booking  
How many guests are you confirming for tonight's event?
Your input ->  160 guests  
And how many of those guests will need vegan meals?
Your input ->  can you arrange parking for the speakers            
I can only help with confirming tonight's venue booking. For anything else, please contact the event organiser directly.              
Would you like to continue with confirm booking?
"""

# Describe what CALM did after the out-of-scope message. Min 20 words.
CONVERSATION_3_WHAT_HAPPENED = """
CALM recognised the parking request as outside the confirm_booking flow scope and routed it to the
handle_out_of_scope flow. It uttered the scripted deflection ("I can only help with confirming tonight's
venue booking") and then asked "Would you like to continue with confirm booking?" — offering to resume
the active flow rather than abandoning the conversation entirely.
"""

# Compare Rasa CALM's handling of the out-of-scope request to what
# LangGraph did in Exercise 2 Scenario 3. Min 40 words.
OUT_OF_SCOPE_COMPARISON = """
In Exercise 2, the LangGraph agent had no explicit out-of-scope handling — when asked about train times
it simply replied it lacked the necessary details and asked the user to rephrase, without acknowledging
the request was off-topic. CALM, by contrast, has an explicit handle_out_of_scope flow: the LLM recognised
the parking request was outside confirm_booking, routed to that flow, delivered a clear deflection message,
and then offered to resume the booking flow. CALM's approach is more structured and user-friendly because
the out-of-scope path is authored explicitly, whereas LangGraph's response was an accidental fallback
with no awareness that the topic had shifted.
"""

# ── Task B: Cutoff guard ───────────────────────────────────────────────────

TASK_B_DONE = True   # True or False

# List every file you changed.
TASK_B_FILES_CHANGED = ["exercise3_rasa/actions/actions.py "]

# How did you test that it works? Min 20 words.
TASK_B_HOW_YOU_TESTED = """
I uncommented code in actions.py file and changed the condition from complex to just True.
After that I ran happy-case scenario to check that in the end of conversation bot would escalate the booking.
"""

# ── CALM vs Old Rasa ───────────────────────────────────────────────────────

# In the old open-source Rasa (3.6.x), you needed:
#   ValidateBookingConfirmationForm with regex to parse "about 160" → 160.0
#   nlu.yml intent examples to classify "I'm calling to confirm"
#   rules.yml to define every dialogue path
#
# In Rasa Pro CALM, you need:
#   flow descriptions so the LLM knows when to trigger confirm_booking
#   from_llm slot mappings so the LLM extracts values from natural speech
#   ONE action class (ActionValidateBooking) for the business rules
#
# What does this simplification cost? What does it gain?
# Min 30 words.

CALM_VS_OLD_RASA = """
The LLM now does what regex and nlu.yml used to do — parsing "about 160 people" into 160.0 and
figuring out the user wants to confirm a booking. Python still handles the business rule guards
(capacity, deposit limit, vegan ratio) because those are deterministic checks the LLM shouldn't
negotiate around. The old regex approach was more predictable, but it would break on anything
you didn't write a pattern for, like "one-sixty" or "roughly 160".
"""

# ── The setup cost ─────────────────────────────────────────────────────────

# CALM still required: config.yml, domain.yml, flows.yml, endpoints.yml,
# rasa train, two terminals, and a Rasa Pro licence.
# The old Rasa ALSO needed nlu.yml, rules.yml, and a FormValidationAction.
#
# CALM is simpler. But it's still significantly more setup than LangGraph.
# That setup bought you something specific.
# Min 40 words.

SETUP_COST_VALUE = """
CALM needs way more config files and a training step compared to LangGraph where you just define
Python functions and go. But the tradeoff is that the CALM agent can't improvise — it can't call a
tool not in flows.yml, can't invent a new conversation path, can't freestyle a response. For booking
confirmation that's exactly what you want. The LangGraph agent could hallucinate a venue or offer
to look up train times, which is great for open-ended research but risky for financially binding
decisions. So the setup cost buys you predictability — every path the agent can take is visible
in flows.yml before you deploy it.
"""

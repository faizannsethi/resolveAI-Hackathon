"""Voice layer: voice intake -> case files -> the unchanged case agent -> MP3 voice update for the tenant.

Kept separate from agent/ and tools/: it only builds case folders the agent already understands and
reads the agent's outputs. Nothing in the core agent was changed to support voice.
"""

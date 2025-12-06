# Template Question Set

This folder contains template questions for "De Slimste Mens Ter Wereld".

## Purpose

This is a **template** folder that serves as a reference for creating new question sets. 
**Do not use this folder directly in the game** - it's meant to be copied when creating new question sets.

## Question Formats

This template includes all 6 question formats used in the game:

### 1. **3-6-9.json** - Simple Question/Answer
```json
{
  "question": "Question text?",
  "answer": "Answer text"
}
```

### 2. **Open deur.json** - Question with Multiple Answers + Media
```json
{
  "image": "image-file.png",
  "question": "Question text?",
  "answers": ["Answer 1", "Answer 2", "Answer 3", "Answer 4"],
  "video": "video-file.mp4"
}
```

### 3. **Collectief geheugen.json** - Answers + Media (No Question)
```json
{
  "image": "image-file.jpg",
  "answers": ["Answer 1", "Answer 2", "Answer 3", "Answer 4", "Answer 5"],
  "video": "video-file.mp4"
}
```

### 4. **Finale.json** - Question with Multiple Answers
```json
{
  "question": "Question text?",
  "answers": ["Answer 1", "Answer 2", "Answer 3", "Answer 4", "Answer 5"]
}
```

### 5. **Galerij.json** - Multiple Images with Answers
```json
{
  "images": ["image1.png", "image2.png", "image3.png", ..., "image10.png"],
  "answers": ["Answer 1", "Answer 2", "Answer 3", ..., "Answer 10"]
}
```

### 6. **Puzzel.json** - Keywords with Answer
```json
{
  "keywords": ["Keyword 1", "Keyword 2", "Keyword 3", "Keyword 4"],
  "answer": "Answer text"
}
```

## Creating a New Question Set

1. Copy this entire `template` folder
2. Rename it to your new question set name (e.g., `christmas-2024`)
3. Edit the JSON files with your own questions
4. Replace the media files (images/videos) with your own
5. The new folder will automatically appear in the game's question set dropdown

## Media Files

- Images should be PNG or JPG format
- Videos should be MP4 format
- Keep file sizes reasonable for web delivery
- Use descriptive filenames that match your JSON references

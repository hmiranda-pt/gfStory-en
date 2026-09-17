# Story Selection Data Source

The story selection hierarchy in the simulator is defined in **`src/assets/chapters.json`**, a generated file consumed by the Vue frontend component `StoryList.vue`. It is produced by a Python build pipeline from raw game data files.

## Data Pipeline

```
Raw game data (.txt)                    Formatted (.hjson)              Generated (JSON)            Frontend (TS/Vue)
─────────────────────                   ─────────────────               ──────────────              ─────────────────
story_playback.txt  ─┐
story_util.txt      ─┼─► chapters.py ──► chapters.json ──► StoryList.vue (tree menu)
mission.txt        ─┘   (unpack/src/      (src/assets/)         (src/components/simulator/)
                       gfunpack/)
```

## Key Files

| Role | File |
|------|------|
| Raw game data (episodes) | `unpack/gf-data-us/asset/table/story_playback.txt` |
| Raw game data (story descriptions) | `unpack/gf-data-us/asset/table/story_util.txt` |
| Raw game data (mission names) | `unpack/gf-data-us/asset/table/mission.txt` |
| Formatted overlay | `unpack/fixed-data/formatted/story_playback.hjson` |
| Python generator | `unpack/src/gfunpack/chapters.py` |
| Manual overrides | `unpack/src/gfunpack/manual_chapters.py` |
| Generated output | `src/assets/chapters.json` |
| TypeScript types | `src/types/assets.ts:45-60` |
| Tree-building UI | `src/components/simulator/StoryList.vue:64-123` |

## The 4-Level Hierarchy

The types in `src/types/assets.ts:45-60`:

```typescript
export type ChapterType = (
  'main' | 'event' | 'colab' | 'bonding' | 'upgrading'
  | 'anniversary' | 'anniversary5' | 'anniversary4' | 'anniversary3' | 'skin'
  | 'help'
);

export type Story = {
  name: string;
  description: string;
  files: (string | string[])[];   // string = filename; string[] = [filename, custom label]
};

export type Chapter = {
  name: string;
  description: string;
  stories: Story[];
};

export type GfChaptersInfo = Record<ChapterType, Chapter[]>;
```

Example mapping:

```
Level 1: Category  (ChapterType key)    → "main"          displayed as "Main Story"
  Level 2: Chapter (Chapter.name)       → "EP. 5.5 Operation Cube"
    Level 3: Story   (Story.name)        → "Seven-Step Puzzle"
      Level 4: Part  (Story.files[i])   → "-1-1-1.txt"    displayed as "Part 1"
```

The actual `chapters.json` content for this example:

```json
{
  "main": [
    {
      "name": "EP. 5.5 Operation Cube",
      "description": "",
      "stories": [
        {
          "name": "Seven-Step Puzzle",
          "description": "After AR-15...",
          "files": ["-1-1-1.txt", "-1-1-2.txt"]
        }
      ]
    }
  ]
}
```

## Naming Conventions Per Level

| Level | Type | Name source | Convention | Example |
|-------|------|-------------|------------|---------|
| **1. Category** | `ChapterType` | Hardcoded in `StoryList.vue:111-122` | Fixed set of 11 keys, each mapped to a display label | `main` → `"Main Story"` |
| **2. Chapter** | `Chapter.name` | Built in `chapters.py` from `story_playback.txt` | `"{tag} {chapter} {name}"` — tag from `story_playback-40000000`, chapter number from `story_playback-20000000`, name from `story_playback-10000000` | `"EP. 5.5 Operation Cube"` |
| **3. Story** | `Story.name` | From `story_util.txt` (`story_util-20000000` = title) or `mission.txt`, with manual overrides from `manual_chapters.py` | Free-text title from game data | `"Seven-Step Puzzle"` |
| **4. Part** | `Story.files[]` | Script filenames parsed from each story event's `scripts`/`first`/`start`/`point`/`round`/`end` fields in `story_util.txt` | Auto-labeled `"Part {i+1}"` in `StoryList.vue:70` when stored as a plain string; or custom label when stored as `[filename, label]` tuple | `"Part 1"`, `"Part 2"` |

## How the UI Builds the Tree (`StoryList.vue:64-123`)

- **Level 4 (Part)** — `generateLeafOption()`: if a file entry is a plain string, it becomes `Part {i+1}`; if it's a `[filename, label]` array, the second element is the custom label.
- **Level 3 (Story)** — `generateStoryOptions()`: if a story has only 1 file, it's a leaf node with no children; if multiple files, it gets child Part nodes. A "Stage selection interface" option is prepended for chapters whose names match known EP prefixes.
- **Level 2 (Chapter)** — `generateChapterOption()`: maps each `Chapter` under its category.
- **Level 1 (Category)** — `rawData` array (line 111): hardcoded list calling `generateChapterOption` for each of the 11 category types with their display labels.

## Raw Data Format (`story_playback.txt`)

```
story_playback-10000001,Chapter 0           ← name (e.g. "Chapter 0", "Operation Cube")
story_playback-20000001,0                  ← chapter number (e.g. "0", "5", "5.5")
story_playback-30000001,                   ← campaign IDs (comma-separated, e.g. "-1")
story_playback-40000001,EP.                ← tag ("EP." or "C.E.")
story_playback-50000001,Normal             ← sub-names (semicolon-separated)
```

The Python generator combines these fields into `"EP. 5.5 Operation Cube"` and uses the campaign ID mapping to group individual `story_util` events under the right chapter.

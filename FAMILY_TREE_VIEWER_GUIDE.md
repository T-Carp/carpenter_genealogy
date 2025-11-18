# Family Tree Viewer Guide

## Overview

The Family Tree Viewer is a standalone HTML application that connects to your FastAPI backend to visualize genealogy data using D3.js. This provides an interactive, browser-based family tree that fetches data in real-time from the API.

## Architecture

```
Browser (family_tree_viewer.html)
    ↓ HTTP Requests
FastAPI Server (http://localhost:8000)
    ↓ Database Queries
SQLite Database (data/structured_db/genealogy.db)
```

## Getting Started

### 1. Start the API Server

First, ensure the FastAPI server is running:

```bash
# Start the server
python api.py --port 8000

# Or with auto-reload for development
python api.py --port 8000 --reload
```

You should see:
```
============================================================
Genealogy API Starting
============================================================
OpenAPI docs: http://localhost:8000/docs
ReDoc docs: http://localhost:8000/redoc
Database: data/structured_db/genealogy.db
============================================================
```

### 2. Open the Viewer

Simply open the HTML file in your web browser:

```bash
# On macOS
open family_tree_viewer.html

# On Linux
xdg-open family_tree_viewer.html

# On Windows
start family_tree_viewer.html
```

Or navigate to the file directly in your browser:
- File: `/Users/troycarpenter/Documents/GitHub/carpenter_genealogy/family_tree_viewer.html`

## Using the Viewer

### Controls

The viewer provides several interactive controls:

#### 1. Search for Person
- Type at least 2 characters to search
- Results populate the "Root Person" dropdown
- Example: Type "Carpenter" to find all Carpenters

#### 2. Root Person
- Select a specific person to center the tree on
- Leave as "All People" to show everyone
- Tip: Use search to find specific people quickly

#### 3. Max Generations
- Controls how many generations to display (1-5)
- Default: 2 generations
- Higher values = more people but may be harder to visualize
- Recommended: 2-3 for best clarity

#### 4. Filter by Surname
- Shows only people with the selected surname
- Useful for isolating specific family lines
- Example: Select "Keenum" to see only the Keenum lineage

#### 5. Include Ancestors
- Checkbox to include ancestors of the root person
- Uncheck to hide parents, grandparents, etc.

#### 6. Include Descendants
- Checkbox to include descendants of the root person
- Uncheck to hide children, grandchildren, etc.

#### 7. Color by Surname
- When checked, colors nodes by surname
- Makes it easy to see different family lines
- Each surname gets a distinct color

### Visualization Features

#### Interactive Tree
- **Pan**: Click and drag to move the tree
- **Zoom**: Use mouse wheel or pinch gesture to zoom in/out
- **Hover**: Hover over nodes to see detailed information
- **Auto-layout**: D3.js automatically arranges nodes hierarchically

#### Node Display
- **Circles**: Represent individual people
- **Lines**: Show parent-child relationships
- **Names**: Display as text labels next to each node
- **Colors**: Vary by surname (if enabled)

#### Tooltip Information
When you hover over a person's node, you'll see:
- Full name
- Birth and death years (if known)
- Additional information

## Example Workflows

### Workflow 1: View a Specific Person's Family

1. Type the person's name in "Search for Person"
2. Select them from the "Root Person" dropdown
3. Set "Max Generations" to 2 or 3
4. Check both "Include Ancestors" and "Include Descendants"
5. Click "Generate Tree"

Result: You'll see the person's parents, grandparents, children, and grandchildren.

### Workflow 2: Explore a Surname

1. Select a surname from "Filter by Surname" (e.g., "Carpenter")
2. Set "Max Generations" to 2
3. Leave "Root Person" as "All People"
4. Check "Color by Surname"
5. Click "Generate Tree"

Result: You'll see all Carpenters in the database with their relationships.

### Workflow 3: View Descendants Only

1. Search for an ancestor (e.g., "Richard Keenum")
2. Select them as "Root Person"
3. Set "Max Generations" to 3
4. Check "Include Descendants" ONLY (uncheck Ancestors)
5. Click "Generate Tree"

Result: You'll see the ancestor and all their descendants going forward in time.

### Workflow 4: View Ancestors Only

1. Search for yourself or a recent family member
2. Select them as "Root Person"
3. Set "Max Generations" to 3
4. Check "Include Ancestors" ONLY (uncheck Descendants)
5. Click "Generate Tree"

Result: You'll see the person and all their ancestors going back in time.

## API Endpoints Used

The viewer uses these FastAPI endpoints:

### 1. `/api/genealogy/surnames`
- Returns list of all unique surnames
- Populates the surname filter dropdown

### 2. `/api/genealogy/search?q={query}&limit={limit}`
- Searches for people by name
- Returns matching results with IDs
- Used by the search functionality

### 3. `/api/genealogy/graph`
Parameters:
- `root_id`: Optional person ID to center on
- `generations`: Max generations to include (1-10)
- `include_ancestors`: Boolean
- `include_descendants`: Boolean
- `surname_filter`: Optional surname to filter by

Returns:
- `nodes`: Array of person objects
- `edges`: Array of relationship objects
- `metadata`: Statistics and metadata

## Troubleshooting

### Issue: "No data found matching criteria"

**Causes:**
- Too restrictive filters
- Root person has no relationships in database
- Database is empty

**Solutions:**
- Try removing filters
- Select "All People" instead of a specific root
- Increase max generations
- Check that database has data

### Issue: Visualization doesn't load

**Causes:**
- API server not running
- Browser blocking local file access
- CORS issues

**Solutions:**
- Verify API is running: `curl http://localhost:8000/api/health`
- Check browser console for errors (F12)
- Ensure API is on port 8000

### Issue: Search doesn't return results

**Causes:**
- Less than 2 characters typed
- Name not in database
- API connectivity issue

**Solutions:**
- Type at least 2 characters
- Try partial names (e.g., "Carp" instead of "Carpenter")
- Check API is running

### Issue: Too many nodes to display

**Problem:**
- If there are more than 200 nodes (currently in code), visualization won't render

**Solution:**
- Reduce max generations
- Select a specific root person
- Use surname filter

## Technical Details

### Data Flow

1. **User clicks "Generate Tree"**
2. **JavaScript builds API URL** with all parameters
3. **Fetch request** sent to FastAPI
4. **API queries database** and builds graph
5. **JSON response** returned with nodes/edges
6. **JavaScript converts** flat graph to hierarchical tree
7. **D3.js renders** the tree visualization

### Tree Conversion Algorithm

The viewer converts the flat graph structure (nodes + edges) into a hierarchical tree:

```javascript
1. Start with root person (or first person with no parents)
2. Recursively traverse relationships
3. Build tree structure: { name, id, children: [...] }
4. D3 hierarchy layout processes the tree
5. Tidy tree algorithm positions nodes
6. SVG elements render the visualization
```

### Browser Compatibility

- Modern browsers (Chrome, Firefox, Safari, Edge)
- Requires JavaScript enabled
- D3.js v7 loaded from CDN
- Responsive design works on desktop and tablet

## Performance Considerations

### Large Datasets

The viewer has built-in limits:
- API limits: Max 10 generations
- Reasonable for datasets up to ~1000 people per query

### Optimization Tips

1. **Use filters**: Reduce data by surname or specific person
2. **Limit generations**: Keep to 2-3 for best performance
3. **Specific root person**: Center on one person instead of "All People"

## API Documentation

For complete API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Next Steps

### Future Enhancements

Possible additions to the viewer:
1. Export to image (PNG, SVG)
2. Collapsible nodes (click to expand/collapse branches)
3. Search within current visualization
4. Filter by date ranges
5. Show additional person details (birth/death places, etc.)
6. Print-friendly view
7. Share links with specific parameters

### Integration with Frontend

This viewer serves as a prototype for a full React/Vue.js application. The same API endpoints can be used in a more sophisticated frontend framework.

## Support

If you encounter issues:
1. Check API server is running
2. Check browser console for errors (F12)
3. Verify database has data: `sqlite3 data/structured_db/genealogy.db "SELECT COUNT(*) FROM persons;"`
4. Test API directly: `curl http://localhost:8000/api/genealogy/graph?generations=2`

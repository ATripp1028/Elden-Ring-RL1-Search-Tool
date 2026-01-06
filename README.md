# Elden Ring RL1 Search Tool

A comprehensive web application designed to help Elden Ring players plan Rune Level 1 (RL1) challenge runs by filtering and searching through all available weapons and spells based on character stat requirements.

## Purpose

In Elden Ring, Rune Level 1 (RL1) runs are challenge runs where players attempt to complete the game without leveling up, keeping all stats at their base values. This tool enables players to quickly find which weapons and spells are available to them at any given stat configuration, accounting for two-handed wielding mechanics and various filtering options to streamline build planning.

## Tech Stack

### Frontend
- **Vue 3** (Composition API with `<script setup>`)
- **TypeScript** - Full type safety across the application
- **Pinia** - State management with modular store architecture
- **PrimeVue** - UI component library for consistent design
- **Vue Router** - Client-side routing
- **Vite** - Fast build tool and development server

### Development Tools
- **Vitest** - Unit testing framework
- **ESLint** + **Prettier** - Code quality and formatting
- **vue-tsc** - TypeScript type checking for Vue components
- **Vue DevTools** - Development debugging support

### Data Processing
- **Python** - Data scraping scripts (`fetch-weapons.py`, `fetch-spells.py`)
  - BeautifulSoup4 for HTML parsing
  - Requests for HTTP operations
  - LXML for efficient parsing

## Features

### Core Functionality
- **Stat-based Filtering**: Input character stats (Strength, Dexterity, Intelligence, Faith, Arcane) to find compatible weapons and spells
- **Two-handed Calculation**: Automatically accounts for 1.5x Strength multiplier when two-handing weapons
- **Dual Data Types**: Search through weapons, spells (sorceries/incantations), or both simultaneously
- **Ignore Stats Mode**: Browse all items ignoring stat requirements for general exploration

### Advanced Filtering
- **Weapon Type Filtering**: Filter by 40+ weapon categories (daggers, greatswords, staves, etc.)
- **Damage Type Filtering**: Filter by Physical, Fire, Lightning, Holy, and Magic damage types
- **Attack Type Filtering**: Filter by Standard, Slash, Strike, and Pierce attack types
- **Status Buildup Filtering**: Filter by bleed, poison, frost, scarlet rot, sleep, and madness buildups
- **DLC Support**: Toggle Shadow of the Erdtree DLC content inclusion
- **Shield Filtering**: Option to hide shields from results

### User Interface
- **Sortable Columns**: Click any column header to sort by that attribute (ascending/descending)
- **Customizable Columns**: Show/hide columns based on user preferences
- **Text Search**: Real-time search filtering across all displayed data
- **Pagination**: Efficient handling of large result sets with configurable items per page
- **Responsive Layout**: Sidebar search form with main content area
- **Accessibility**: Helpful tooltips and clear UI labels

### Data Management
- **Comprehensive Dataset**: Includes all base game and DLC weapons and spells
- **Structured JSON Data**: Organized by weapon type for efficient loading
- **Local Storage**: Persistent user preferences (if implemented)
- **Type-safe Data Models**: Strong TypeScript interfaces for all data structures

## Project Structure

```
src/
├── components/          # Vue components
│   ├── base/           # Reusable base components (MultiSelect, Pagination)
│   ├── icons/          # Icon components
│   ├── SearchForm.vue  # Main search interface
│   ├── ResultsFilter.vue # Table filtering and column controls
│   └── WeaponsTable.vue # Data display table
├── stores/             # Pinia state management
│   ├── modules/        # Modular stores (filters, pagination, stats, UI, weapons)
│   └── index.ts        # Store exports
├── model/              # TypeScript types and constants
├── utils/              # Data loading utilities
├── resources/          # JSON data files (weapons and spells)
├── composables/        # Vue composition functions
├── assets/             # Styles and static assets
└── fetch-*.py          # Python data scraping scripts
```

## Setup & Installation

### Prerequisites
- **Node.js** (v18+ recommended)
- **npm** or **yarn**
- **Python 3.8+** (for data scraping scripts, if needed)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Elden-Ring-RL1-Search-Tool
```

2. Install dependencies:
```bash
npm install
```

3. (Optional) Install Python dependencies for data scraping:
```bash
pip install -r requirements.txt
```

### Development

Start the development server with hot-reload:
```bash
npm run dev
```

The application will be available at `http://localhost:5173` (or the next available port).

### Building for Production

Type-check, compile, and minify for production:
```bash
npm run build
```

Preview the production build:
```bash
npm run preview
```

### Testing

Run unit tests:
```bash
npm run test:unit
```

### Code Quality

Lint code:
```bash
npm run lint
```

Format code:
```bash
npm run format
```

Type checking:
```bash
npm run type-check
```

## Architecture Highlights

- **Modular State Management**: Separated concerns across multiple Pinia stores (filters, pagination, stats, UI, weapons) for maintainability
- **Type Safety**: Comprehensive TypeScript coverage with strict typing for all data models and component props
- **Component Composition**: Reusable base components (BaseMultiSelect, BasePagination) following DRY principles
- **Performance**: Efficient data loading and filtering with computed properties and reactive state
- **Scalability**: Modular architecture makes it easy to add new weapon types, filters, or data sources

## Data Sources

Weapon and spell data is scraped from Elden Ring wiki sources using Python scripts. The data is then processed into structured JSON files organized by weapon type for efficient loading in the frontend application.

## Contributing

This is a personal project, but suggestions and feedback are welcome. Please ensure all code follows the existing style guide and passes linting/type checking before submitting.

## License

See [LICENSE](LICENSE) file for details.

## Author

Made by MrSporkMan (Alex Tripp)

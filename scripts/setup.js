
const db = require('better-sqlite3')('./learn-anywhere.db');
const fs = require('fs');

try {
  const createTablesSql = fs.readFileSync('scripts/01-create-tables.sql', 'utf8');
  db.exec(createTablesSql);
  console.log('Tables created successfully.');

  const seedSubjectsSql = fs.readFileSync('scripts/02-seed-subjects.sql', 'utf8');
  db.exec(seedSubjectsSql);
  console.log('Subjects seeded successfully.');

  console.log('Database setup complete.');
} catch (err) {
  console.error('Error setting up database:', err.message);
} finally {
  db.close();
}

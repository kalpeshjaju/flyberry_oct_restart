#!/usr/bin/env node

/**
 * Data Validation Script for Flyberry Extracted Data
 *
 * Validates all extracted JSON files against their schemas
 * Reports validation errors and generates summary
 */

const fs = require('fs');
const path = require('path');

// Simple JSON Schema validator (subset implementation)
function validateSchema(data, schema, filePath = '') {
  const errors = [];

  function validate(value, schemaNode, currentPath) {
    // Type validation
    if (schemaNode.type) {
      const actualType = Array.isArray(value) ? 'array' : typeof value;
      // JSON doesn't distinguish between integer and number - treat integer schema as number
      const normalizedSchemaType = schemaNode.type === 'integer' ? 'number' : schemaNode.type;
      const normalizedActualType = actualType;

      if (normalizedActualType !== normalizedSchemaType && !(value === null && schemaNode.type === 'object')) {
        errors.push(`${currentPath}: Expected type ${schemaNode.type}, got ${actualType}`);
        return;
      }

      // Additional check for integer: must be whole number
      if (schemaNode.type === 'integer' && typeof value === 'number' && !Number.isInteger(value)) {
        errors.push(`${currentPath}: Expected integer, got decimal ${value}`);
        return;
      }
    }

    // Required fields
    if (schemaNode.required && schemaNode.type === 'object') {
      for (const field of schemaNode.required) {
        if (!(field in value)) {
          errors.push(`${currentPath}: Missing required field '${field}'`);
        }
      }
    }

    // Properties validation
    if (schemaNode.properties && typeof value === 'object' && !Array.isArray(value)) {
      for (const [key, val] of Object.entries(value)) {
        if (schemaNode.properties[key]) {
          validate(val, schemaNode.properties[key], `${currentPath}.${key}`);
        }
      }
    }

    // Array validation
    if (schemaNode.type === 'array' && Array.isArray(value)) {
      if (schemaNode.minItems && value.length < schemaNode.minItems) {
        errors.push(`${currentPath}: Array must have at least ${schemaNode.minItems} items, has ${value.length}`);
      }
      if (schemaNode.items) {
        value.forEach((item, index) => {
          validate(item, schemaNode.items, `${currentPath}[${index}]`);
        });
      }
    }

    // String validations
    if (schemaNode.type === 'string' && typeof value === 'string') {
      if (schemaNode.minLength && value.length < schemaNode.minLength) {
        errors.push(`${currentPath}: String must be at least ${schemaNode.minLength} characters, got ${value.length}`);
      }
      if (schemaNode.maxLength && value.length > schemaNode.maxLength) {
        errors.push(`${currentPath}: String must be at most ${schemaNode.maxLength} characters, got ${value.length}`);
      }
      if (schemaNode.pattern) {
        const regex = new RegExp(schemaNode.pattern);
        if (!regex.test(value)) {
          errors.push(`${currentPath}: String does not match pattern ${schemaNode.pattern}: "${value}"`);
        }
      }
    }

    // Number validations
    if (schemaNode.type === 'number' && typeof value === 'number') {
      if (schemaNode.minimum !== undefined && value < schemaNode.minimum) {
        errors.push(`${currentPath}: Number must be at least ${schemaNode.minimum}, got ${value}`);
      }
      if (schemaNode.maximum !== undefined && value > schemaNode.maximum) {
        errors.push(`${currentPath}: Number must be at most ${schemaNode.maximum}, got ${value}`);
      }
    }

    // Enum validation
    if (schemaNode.enum && !schemaNode.enum.includes(value)) {
      errors.push(`${currentPath}: Value must be one of [${schemaNode.enum.join(', ')}], got "${value}"`);
    }
  }

  validate(data, schema, filePath || 'root');
  return errors;
}

// Main validation function
function validateAllData() {
  console.log('🔍 Validating Flyberry Extracted Data...\n');

  const baseDir = path.join(__dirname, 'extracted_data');
  const schemasDir = path.join(baseDir, 'schemas');

  // Load schemas
  const productSchema = JSON.parse(fs.readFileSync(path.join(schemasDir, 'product-schema.json'), 'utf8'));
  const recipeSchema = JSON.parse(fs.readFileSync(path.join(schemasDir, 'recipe-schema.json'), 'utf8'));
  const designSchema = JSON.parse(fs.readFileSync(path.join(schemasDir, 'design-schema.json'), 'utf8'));

  const results = {
    products: { total: 0, valid: 0, errors: [] },
    recipes: { total: 0, valid: 0, errors: [] },
    design: { total: 0, valid: 0, errors: [] }
  };

  // Validate products
  console.log('📦 Validating Products...');
  const productsDir = path.join(baseDir, 'products');
  const productFiles = fs.readdirSync(productsDir).filter(f => f.endsWith('.json') && f !== 'index.json');

  for (const file of productFiles) {
    results.products.total++;
    const filePath = path.join(productsDir, file);
    const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));
    const errors = validateSchema(data, productSchema, file);

    if (errors.length === 0) {
      results.products.valid++;
      console.log(`  ✅ ${file}`);
    } else {
      console.log(`  ❌ ${file} (${errors.length} errors)`);
      results.products.errors.push({ file, errors });
    }
  }

  // Validate recipes
  console.log('\n🍳 Validating Recipes...');
  const recipesDir = path.join(baseDir, 'recipes');
  const recipeFiles = fs.readdirSync(recipesDir).filter(f => f.endsWith('.json') && f !== 'index.json');

  for (const file of recipeFiles) {
    results.recipes.total++;
    const filePath = path.join(recipesDir, file);
    const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));
    const errors = validateSchema(data, recipeSchema, file);

    if (errors.length === 0) {
      results.recipes.valid++;
      console.log(`  ✅ ${file}`);
    } else {
      console.log(`  ❌ ${file} (${errors.length} errors)`);
      results.recipes.errors.push({ file, errors });
    }
  }

  // Validate design system
  console.log('\n🎨 Validating Design System...');
  const designFile = path.join(baseDir, 'design', 'brand-design-system.json');
  results.design.total++;
  const designData = JSON.parse(fs.readFileSync(designFile, 'utf8'));
  const designErrors = validateSchema(designData, designSchema, 'brand-design-system.json');

  if (designErrors.length === 0) {
    results.design.valid++;
    console.log(`  ✅ brand-design-system.json`);
  } else {
    console.log(`  ❌ brand-design-system.json (${designErrors.length} errors)`);
    results.design.errors.push({ file: 'brand-design-system.json', errors: designErrors });
  }

  // Summary
  console.log('\n' + '='.repeat(60));
  console.log('📊 VALIDATION SUMMARY');
  console.log('='.repeat(60));
  console.log(`Products:  ${results.products.valid}/${results.products.total} valid`);
  console.log(`Recipes:   ${results.recipes.valid}/${results.recipes.total} valid`);
  console.log(`Design:    ${results.design.valid}/${results.design.total} valid`);

  const totalValid = results.products.valid + results.recipes.valid + results.design.valid;
  const totalFiles = results.products.total + results.recipes.total + results.design.total;

  console.log(`\nTotal:     ${totalValid}/${totalFiles} files valid`);

  // Show detailed errors if any
  const allErrors = [...results.products.errors, ...results.recipes.errors, ...results.design.errors];
  if (allErrors.length > 0) {
    console.log('\n' + '='.repeat(60));
    console.log('❌ VALIDATION ERRORS');
    console.log('='.repeat(60));

    for (const { file, errors } of allErrors) {
      console.log(`\n${file}:`);
      errors.forEach(err => console.log(`  - ${err}`));
    }

    process.exit(1);
  } else {
    console.log('\n✅ All data files are valid!');
    process.exit(0);
  }
}

// Run validation
try {
  validateAllData();
} catch (error) {
  console.error('❌ Validation failed with error:', error.message);
  console.error(error.stack);
  process.exit(1);
}

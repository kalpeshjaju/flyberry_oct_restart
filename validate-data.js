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
  const giftingSchema = JSON.parse(fs.readFileSync(path.join(schemasDir, 'gifting-catalogue-schema.json'), 'utf8'));
  const retailSchema = JSON.parse(fs.readFileSync(path.join(schemasDir, 'retail-catalogue-schema.json'), 'utf8'));
  const investorSchema = JSON.parse(fs.readFileSync(path.join(schemasDir, 'investor-updates-schema.json'), 'utf8'));
  const claimsSchema = JSON.parse(fs.readFileSync(path.join(schemasDir, 'claims-registry-schema.json'), 'utf8'));

  const results = {
    products: { total: 0, valid: 0, errors: [] },
    recipes: { total: 0, valid: 0, errors: [] },
    design: { total: 0, valid: 0, errors: [] },
    gifting: { total: 0, valid: 0, errors: [] },
    retail: { total: 0, valid: 0, errors: [] },
    investor: { total: 0, valid: 0, errors: [] },
    claims: { total: 0, valid: 0, errors: [] }
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

  // Validate gifting catalogue
  console.log('\n🎁 Validating Gifting Catalogue...');
  const giftingFile = path.join(baseDir, 'gifting-catalogue.json');
  results.gifting.total++;
  const giftingData = JSON.parse(fs.readFileSync(giftingFile, 'utf8'));
  const giftingErrors = validateSchema(giftingData, giftingSchema, 'gifting-catalogue.json');

  if (giftingErrors.length === 0) {
    results.gifting.valid++;
    console.log(`  ✅ gifting-catalogue.json`);
  } else {
    console.log(`  ❌ gifting-catalogue.json (${giftingErrors.length} errors)`);
    results.gifting.errors.push({ file: 'gifting-catalogue.json', errors: giftingErrors });
  }

  // Validate retail catalogue
  console.log('\n🏪 Validating Retail Catalogue...');
  const retailFile = path.join(baseDir, 'retail-catalogue.json');
  results.retail.total++;
  const retailData = JSON.parse(fs.readFileSync(retailFile, 'utf8'));
  const retailErrors = validateSchema(retailData, retailSchema, 'retail-catalogue.json');

  if (retailErrors.length === 0) {
    results.retail.valid++;
    console.log(`  ✅ retail-catalogue.json`);
  } else {
    console.log(`  ❌ retail-catalogue.json (${retailErrors.length} errors)`);
    results.retail.errors.push({ file: 'retail-catalogue.json', errors: retailErrors });
  }

  // Validate investor updates
  console.log('\n📈 Validating Investor Updates...');
  const investorFile = path.join(baseDir, 'investor-updates.json');
  results.investor.total++;
  const investorData = JSON.parse(fs.readFileSync(investorFile, 'utf8'));
  const investorErrors = validateSchema(investorData, investorSchema, 'investor-updates.json');

  if (investorErrors.length === 0) {
    results.investor.valid++;
    console.log(`  ✅ investor-updates.json`);
  } else {
    console.log(`  ❌ investor-updates.json (${investorErrors.length} errors)`);
    results.investor.errors.push({ file: 'investor-updates.json', errors: investorErrors });
  }

  // Validate claims registry
  console.log('\n📋 Validating Claims Registry...');
  const claimsFile = path.join(baseDir, 'claims-registry.json');
  results.claims.total++;
  const claimsData = JSON.parse(fs.readFileSync(claimsFile, 'utf8'));
  const claimsErrors = validateSchema(claimsData, claimsSchema, 'claims-registry.json');

  if (claimsErrors.length === 0) {
    results.claims.valid++;
    console.log(`  ✅ claims-registry.json`);
  } else {
    console.log(`  ❌ claims-registry.json (${claimsErrors.length} errors)`);
    results.claims.errors.push({ file: 'claims-registry.json', errors: claimsErrors });
  }

  // Summary
  console.log('\n' + '='.repeat(60));
  console.log('📊 VALIDATION SUMMARY');
  console.log('='.repeat(60));
  console.log(`Products:  ${results.products.valid}/${results.products.total} valid`);
  console.log(`Recipes:   ${results.recipes.valid}/${results.recipes.total} valid`);
  console.log(`Design:    ${results.design.valid}/${results.design.total} valid`);
  console.log(`Gifting:   ${results.gifting.valid}/${results.gifting.total} valid`);
  console.log(`Retail:    ${results.retail.valid}/${results.retail.total} valid`);
  console.log(`Investor:  ${results.investor.valid}/${results.investor.total} valid`);
  console.log(`Claims:    ${results.claims.valid}/${results.claims.total} valid`);

  const totalValid = results.products.valid + results.recipes.valid + results.design.valid +
                     results.gifting.valid + results.retail.valid + results.investor.valid + results.claims.valid;
  const totalFiles = results.products.total + results.recipes.total + results.design.total +
                     results.gifting.total + results.retail.total + results.investor.total + results.claims.total;

  console.log(`\nTotal:     ${totalValid}/${totalFiles} files valid`);

  // Show detailed errors if any
  const allErrors = [...results.products.errors, ...results.recipes.errors, ...results.design.errors,
                      ...results.gifting.errors, ...results.retail.errors, ...results.investor.errors, ...results.claims.errors];
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

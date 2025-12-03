/**
 * Example usage of the CQL executor functions.
 * 
 * This demonstrates how to:
 * 1. Create a reusable executor for a measure
 * 2. Execute the measure against patient data
 * 3. Use value sets with the executor
 */

import { createMeasureExecutor, executeMeasureOnce } from './cqlExecutor.js';

// Example: Creating a reusable executor for a measure
export async function exampleReusableExecutor() {
  // Load your ELM measure (converted from CQL)
  const elmMeasure = {
    library: {
      identifier: { id: 'MyMeasure', version: '1.0.0' },
      // ... rest of ELM structure
    }
  };

  // Define value sets (format depends on cql-execution requirements)
  // Typically, value sets are keyed by OID or URL
  const valueSets = {
    'urn:oid:1.3.6.1.4.1.33895.1.3.0.45': {
      // Value set definition structure
      // This format may need to match cql-execution's expected format
    }
  };

  // Create executor once (reusable for multiple patients)
  const executor = createMeasureExecutor(elmMeasure, valueSets);

  // Execute against multiple patients
  const patient1 = { id: '1', recordType: 'Patient', /* ... */ };
  const patient2 = { id: '2', recordType: 'Patient', /* ... */ };

  const results1 = await executor(patient1);
  const results2 = await executor(patient2);

  return { results1, results2 };
}

// Example: One-time execution
export async function exampleOneTimeExecution() {
  const elmMeasure = { /* ... */ };
  const patient = { /* ... */ };
  const valueSets = { /* ... */ };

  const results = await executeMeasureOnce(elmMeasure, patient, valueSets);
  return results;
}


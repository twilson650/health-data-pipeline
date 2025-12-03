import { test } from 'node:test';
import assert from 'node:assert';
import { createMeasureExecutor, executeMeasureOnce } from './cqlExecutor.js';

// Example minimal ELM measure for testing
const exampleELM = {
  library: {
    identifier: {
      id: 'TestMeasure',
      version: '1.0.0'
    },
    schemaIdentifier: {
      id: 'urn:hl7-org:elm',
      version: 'r1'
    },
    usings: {
      def: [
        {
          localIdentifier: 'System',
          uri: 'urn:hl7-org:elm-types:r1'
        },
        {
          localIdentifier: 'QDM',
          uri: 'urn:healthit-gov:qdm:v5_3',
          version: '5.3'
        }
      ]
    },
    statements: {
      def: [
        {
          name: 'TestExpression',
          context: 'Patient',
          accessLevel: 'Public',
          expression: {
            type: 'Literal',
            valueType: '{urn:hl7-org:elm-types:r1}Boolean',
            value: 'true'
          }
        }
      ]
    }
  }
};

// Example patient data
const examplePatient = {
  id: '1',
  recordType: 'Patient',
  name: 'Test Patient',
  gender: 'M',
  birthDate: '1980-01-01'
};

// Example value sets (empty for now, can be expanded)
const exampleValueSets = {};

test('createMeasureExecutor returns a function', () => {
  const executor = createMeasureExecutor(exampleELM, exampleValueSets);
  assert.strictEqual(typeof executor, 'function');
});

test('executor function can be called with patient data', async () => {
  const executor = createMeasureExecutor(exampleELM, exampleValueSets);
  const results = await executor(examplePatient);
  assert.ok(results !== undefined);
  assert.ok(results !== null);
});

test('executeMeasureOnce convenience function works', async () => {
  const results = await executeMeasureOnce(exampleELM, examplePatient, exampleValueSets);
  assert.ok(results !== undefined);
  assert.ok(results !== null);
});

test('executor handles array of patients', async () => {
  const executor = createMeasureExecutor(exampleELM, exampleValueSets);
  const patients = [examplePatient, { ...examplePatient, id: '2' }];
  const results = await executor(patients);
  assert.ok(results !== undefined);
});


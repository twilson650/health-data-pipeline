import { Library, Executor, PatientSource, CodeService } from 'cql-execution';

/**
 * Creates a CQL executor for a specific measure.
 * This executor is configured with the measure ELM and value sets,
 * and can be reused to execute the measure against multiple patients.
 *
 * @param {Object} elmMeasure - The ELM (JSON) representation of the CQL measure
 * @param {Object} valueSets - JSON object mapping value set OIDs to their definitions
 * @returns {Function} A function that takes a patient JSON and returns execution results
 */
export function createMeasureExecutor(elmMeasure, valueSets = {}) {
  // Create a CodeService from the value sets
  const codeService = new CodeService(valueSets);

  // Create a Library from the ELM measure
  const library = new Library(elmMeasure);

  // Create an Executor with the library and code service
  const executor = new Executor(library, codeService);

  /**
   * Executes the measure against a patient record.
   *
   * @param {Object|Array} patientData - Single patient JSON object or array of patient objects
   * @returns {Promise<Object>} The execution results
   */
  return async function executeMeasure(patientData) {
    // Convert single patient to array if needed
    const patients = Array.isArray(patientData) ? patientData : [patientData];

    // Create a PatientSource from the patient data
    const patientSource = new PatientSource(patients);

    // Execute the measure
    const results = await executor.exec(patientSource);

    return results;
  };
}

/**
 * Convenience function to execute a measure in one call.
 * Creates an executor and immediately executes with the patient data.
 *
 * @param {Object} elmMeasure - The ELM (JSON) representation of the CQL measure
 * @param {Object} patientData - Single patient JSON object or array of patient objects
 * @param {Object} valueSets - JSON object mapping value set OIDs to their definitions
 * @returns {Promise<Object>} The execution results
 */
export async function executeMeasureOnce(elmMeasure, patientData, valueSets = {}) {
  const executor = createMeasureExecutor(elmMeasure, valueSets);
  return executor(patientData);
}


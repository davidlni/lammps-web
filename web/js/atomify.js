var maxNumAtoms = 10;
var currentScript = ""
var lammpsPtr = -1

var md = {
	runCommands: Module.cwrap('runCommands', 'void', ['string']),
	active: Module.cwrap('active', 'bool', []),
	reset: Module.cwrap('reset', 'number', []),
	runDefault: Module.cwrap('runDefaultScript', 'void', []),
	numberOfAtoms: Module.cwrap('numberOfAtoms', 'number', []),
	systemSizeX: Module.cwrap('systemSizeX', 'number', []),
	systemSizeY: Module.cwrap('systemSizeY', 'number', []),
	systemSizeZ: Module.cwrap('systemSizeZ', 'number', []),
	positions: Module.cwrap('positions', 'number', []),
	x: Module.cwrap('x', 'number', []),
	v: Module.cwrap('v', 'number', []),
	f: Module.cwrap('f', 'number', []),
	lammps_command: Module.cwrap("lammps_command", "number", ["number", "string"]),
	lammps_commands_string: Module.cwrap("lammps_commands_string", "void" , ["number", "string"]),
	lammps_extract_setting: Module.cwrap("lammps_extract_setting", "number" , ["number", "string"]),
	lammps_get_natoms: Module.cwrap("lammps_get_natoms", "number" , ["number"]),
	lammps_extract_global: Module.cwrap("lammps_extract_global", "number", ["number", "string"]),
	lammps_extract_atom: Module.cwrap("lammps_extract_atom", "number", ["number", "string"]),
	lammps_extract_compute: Module.cwrap("lammps_extract_compute", "number", ["number", "string", "number", "number"]),
	lammps_extract_fix: Module.cwrap("lammps_extract_fix", "number", ["number", "string", "number", "number", "number", "number"]),
	lammps_extract_variable: Module.cwrap("lammps_extract_variable", "number", ["number", "string", "string"]),
	lammps_set_variable: Module.cwrap("lammps_set_variable", "number" , ["number", "string", "string"]),
	lammps_get_thermo: Module.cwrap("lammps_get_thermo", "number" , ["number", "string"]),
	lammps_has_error: Module.cwrap("lammps_has_error", "number" , ["number"]),
	lammps_get_last_error_message: Module.cwrap("lammps_get_last_error_message", "number" , ["number", "string", "number"]),
	initialized: false
}

var runScript = function() {
	setTimeout(
		function() { 
			if(lammpsPtr === -1) {
				lammpsPtr = md.reset()
			} else if(md.active()) {
				lammpsPtr = md.reset()
			}
			md.runCommands(currentScript)
			
			if(!md.initialized) {
				md.initialized = true
				animate()
			}
		}, 500);
}

function systemSize() {
	return new THREE.Vector3(md.systemSizeX(), md.systemSizeY(), md.systemSizeZ());;
}

function systemSizeHalf() {
	return systemSize().multiplyScalar(0.5);
}
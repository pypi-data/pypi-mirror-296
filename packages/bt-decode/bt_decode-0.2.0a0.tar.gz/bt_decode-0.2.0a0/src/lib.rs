use codec::{Decode, Encode};
use custom_derive::pydecode;
use frame_metadata::{RuntimeMetadata, RuntimeMetadataPrefixed};

use pyo3::prelude::*;

// Implements ToPyObject for Compact<T> where T is an unsigned integer.
macro_rules! impl_UnsignedCompactIntoPy {
    ( $($type:ty),* $(,)? ) => {
        $(
            impl IntoPy<PyObject> for Compact<$type> {
                fn into_py(self, py: Python<'_>) -> PyObject {
                    let value: $type = self.0.into();

                    value.into_py(py)
                }
            }
        )*
    };
}

#[derive(Clone, Encode, Decode, Copy, Debug, PartialEq, Eq, PartialOrd, Ord)]
struct Compact<T>(pub codec::Compact<T>);
impl_UnsignedCompactIntoPy!(u8, u16, u32, u64, u128);

type AccountId = [u8; 32];

mod dyndecoder;

#[pymodule(name = "bt_decode")]
mod bt_decode {
    use std::collections::HashMap;

    use dyndecoder::{fill_memo_using_well_known_types, get_type_id_from_type_string};
    use frame_metadata::v15::RuntimeMetadataV15;
    use pyo3::types::{PyDict, PyTuple};
    use scale_value::{self, scale::decode_as_type, Composite, Primitive, Value, ValueDef};

    use super::*;

    #[pyclass(name = "AxonInfo", get_all)]
    #[derive(Clone, Encode, Decode)]
    struct AxonInfo {
        ///  Axon serving block.
        pub block: u64,
        ///  Axon version
        pub version: u32,
        ///  Axon u128 encoded ip address of type v6 or v4.
        pub ip: u128,
        ///  Axon u16 encoded port.
        pub port: u16,
        ///  Axon ip type, 4 for ipv4 and 6 for ipv6.
        pub ip_type: u8,
        ///  Axon protocol. TCP, UDP, other.
        pub protocol: u8,
        ///  Axon proto placeholder 1.
        pub placeholder1: u8,
        ///  Axon proto placeholder 2.
        pub placeholder2: u8,
    }

    #[pydecode]
    #[pymethods]
    impl AxonInfo {}

    #[pyclass(name = "PrometheusInfo", get_all)]
    #[derive(Clone, Encode, Decode)]
    struct PrometheusInfo {
        /// Prometheus serving block.
        pub block: u64,
        /// Prometheus version.
        pub version: u32,
        ///  Prometheus u128 encoded ip address of type v6 or v4.
        pub ip: u128,
        ///  Prometheus u16 encoded port.
        pub port: u16,
        /// Prometheus ip type, 4 for ipv4 and 6 for ipv6.
        pub ip_type: u8,
    }

    #[pydecode]
    #[pymethods]
    impl PrometheusInfo {}

    #[pyclass(name = "NeuronInfo", get_all)]
    #[derive(Clone, Encode, Decode)]
    struct NeuronInfo {
        hotkey: AccountId,
        coldkey: AccountId,
        uid: Compact<u16>,
        netuid: Compact<u16>,
        active: bool,
        axon_info: AxonInfo,
        prometheus_info: PrometheusInfo,
        stake: Vec<(AccountId, Compact<u64>)>, // map of coldkey to stake on this neuron/hotkey (includes delegations)
        rank: Compact<u16>,
        emission: Compact<u64>,
        incentive: Compact<u16>,
        consensus: Compact<u16>,
        trust: Compact<u16>,
        validator_trust: Compact<u16>,
        dividends: Compact<u16>,
        last_update: Compact<u64>,
        validator_permit: bool,
        weights: Vec<(Compact<u16>, Compact<u16>)>, // Vec of (uid, weight)
        bonds: Vec<(Compact<u16>, Compact<u16>)>,   // Vec of (uid, bond)
        pruning_score: Compact<u16>,
    }

    #[pydecode]
    #[pymethods]
    impl NeuronInfo {}

    #[pyclass(name = "NeuronInfoLite", get_all)]
    #[derive(Clone, Encode, Decode)]
    struct NeuronInfoLite {
        hotkey: AccountId,
        coldkey: AccountId,
        uid: Compact<u16>,
        netuid: Compact<u16>,
        active: bool,
        axon_info: AxonInfo,
        prometheus_info: PrometheusInfo,
        stake: Vec<(AccountId, Compact<u64>)>, // map of coldkey to stake on this neuron/hotkey (includes delegations)
        rank: Compact<u16>,
        emission: Compact<u64>,
        incentive: Compact<u16>,
        consensus: Compact<u16>,
        trust: Compact<u16>,
        validator_trust: Compact<u16>,
        dividends: Compact<u16>,
        last_update: Compact<u64>,
        validator_permit: bool,
        // has no weights or bonds
        pruning_score: Compact<u16>,
    }

    #[pydecode]
    #[pymethods]
    impl NeuronInfoLite {}

    #[pyclass(name = "SubnetIdentity", get_all)]
    #[derive(Clone, Encode, Decode)]
    struct SubnetIdentity {
        subnet_name: Vec<u8>,
        /// The github repository associated with the chain identity
        github_repo: Vec<u8>,
        /// The subnet's contact
        subnet_contact: Vec<u8>,
    }

    #[pydecode]
    #[pymethods]
    impl SubnetIdentity {}

    #[pyclass(name = "SubnetInfo", get_all)]
    #[derive(Clone, Encode, Decode)]
    struct SubnetInfo {
        netuid: Compact<u16>,
        rho: Compact<u16>,
        kappa: Compact<u16>,
        difficulty: Compact<u64>,
        immunity_period: Compact<u16>,
        max_allowed_validators: Compact<u16>,
        min_allowed_weights: Compact<u16>,
        max_weights_limit: Compact<u16>,
        scaling_law_power: Compact<u16>,
        subnetwork_n: Compact<u16>,
        max_allowed_uids: Compact<u16>,
        blocks_since_last_step: Compact<u64>,
        tempo: Compact<u16>,
        network_modality: Compact<u16>,
        network_connect: Vec<[u16; 2]>,
        emission_values: Compact<u64>,
        burn: Compact<u64>,
        owner: AccountId,
    }

    #[pydecode]
    #[pymethods]
    impl SubnetInfo {
        #[pyo3(name = "decode_vec_option")]
        #[staticmethod]
        fn py_decode_vec_option(encoded: &[u8]) -> Vec<Option<SubnetInfo>> {
            Vec::<Option<SubnetInfo>>::decode(&mut &encoded[..])
                .expect("Failed to decode Vec<Option<SubnetInfo>>")
        }
    }

    #[pyclass(name = "SubnetInfoV2", get_all)]
    #[derive(Clone, Encode, Decode)]
    struct SubnetInfoV2 {
        netuid: Compact<u16>,
        rho: Compact<u16>,
        kappa: Compact<u16>,
        difficulty: Compact<u64>,
        immunity_period: Compact<u16>,
        max_allowed_validators: Compact<u16>,
        min_allowed_weights: Compact<u16>,
        max_weights_limit: Compact<u16>,
        scaling_law_power: Compact<u16>,
        subnetwork_n: Compact<u16>,
        max_allowed_uids: Compact<u16>,
        blocks_since_last_step: Compact<u64>,
        tempo: Compact<u16>,
        network_modality: Compact<u16>,
        network_connect: Vec<[u16; 2]>,
        emission_values: Compact<u64>,
        burn: Compact<u64>,
        owner: AccountId,
        identity: Option<SubnetIdentity>,
    }

    #[pydecode]
    #[pymethods]
    impl SubnetInfoV2 {
        #[pyo3(name = "decode_vec_option")]
        #[staticmethod]
        fn py_decode_vec_option(encoded: &[u8]) -> Vec<Option<SubnetInfoV2>> {
            Vec::<Option<SubnetInfoV2>>::decode(&mut &encoded[..])
                .expect("Failed to decode Vec<Option<SubnetInfoV2>>")
        }
    }

    #[pyclass(name = "SubnetHyperparameters", get_all)]
    #[derive(Decode, Encode, Clone, Debug)]
    pub struct SubnetHyperparams {
        rho: Compact<u16>,
        kappa: Compact<u16>,
        immunity_period: Compact<u16>,
        min_allowed_weights: Compact<u16>,
        max_weights_limit: Compact<u16>,
        tempo: Compact<u16>,
        min_difficulty: Compact<u64>,
        max_difficulty: Compact<u64>,
        weights_version: Compact<u64>,
        weights_rate_limit: Compact<u64>,
        adjustment_interval: Compact<u16>,
        activity_cutoff: Compact<u16>,
        registration_allowed: bool,
        target_regs_per_interval: Compact<u16>,
        min_burn: Compact<u64>,
        max_burn: Compact<u64>,
        bonds_moving_avg: Compact<u64>,
        max_regs_per_block: Compact<u16>,
        serving_rate_limit: Compact<u64>,
        max_validators: Compact<u16>,
        adjustment_alpha: Compact<u64>,
        difficulty: Compact<u64>,
        commit_reveal_weights_interval: Compact<u64>,
        commit_reveal_weights_enabled: bool,
        alpha_high: Compact<u16>,
        alpha_low: Compact<u16>,
        liquid_alpha_enabled: bool,
    }

    #[pydecode]
    #[pymethods]
    impl SubnetHyperparams {}

    #[pyclass(get_all)]
    #[derive(Decode, Encode, Clone, Debug)]
    struct StakeInfo {
        hotkey: AccountId,
        coldkey: AccountId,
        stake: Compact<u64>,
    }

    #[pydecode]
    #[pymethods]
    impl StakeInfo {
        #[pyo3(name = "decode_vec_tuple_vec")]
        #[staticmethod]
        fn py_decode_vec_tuple_vec(encoded: &[u8]) -> Vec<(AccountId, Vec<StakeInfo>)> {
            Vec::<(AccountId, Vec<StakeInfo>)>::decode(&mut &encoded[..])
                .expect("Failed to decode Vec<(AccountId, Vec<StakeInfo>)>")
        }
    }

    #[pyclass(get_all)]
    #[derive(Decode, Encode, Clone, Debug)]
    struct DelegateInfo {
        delegate_ss58: AccountId,
        take: Compact<u16>,
        nominators: Vec<(AccountId, Compact<u64>)>, // map of nominator_ss58 to stake amount
        owner_ss58: AccountId,
        registrations: Vec<Compact<u16>>, // Vec of netuid this delegate is registered on
        validator_permits: Vec<Compact<u16>>, // Vec of netuid this delegate has validator permit on
        return_per_1000: Compact<u64>, // Delegators current daily return per 1000 TAO staked minus take fee
        total_daily_return: Compact<u64>, // Delegators current daily return
    }

    #[pydecode]
    #[pymethods]
    impl DelegateInfo {
        #[pyo3(name = "decode_delegated")]
        #[staticmethod]
        fn py_decode_delegated(encoded: &[u8]) -> Vec<(DelegateInfo, Compact<u64>)> {
            Vec::<(DelegateInfo, Compact<u64>)>::decode(&mut &encoded[..])
                .expect("Failed to decode Vec<(DelegateInfo, Compact<u64>)>")
        }
    }

    #[pyclass(name = "MetadataV15")]
    #[derive(Clone, Encode, Decode, Debug)]
    struct PyMetadataV15 {
        metadata: RuntimeMetadataV15,
    }

    #[pymethods]
    impl PyMetadataV15 {
        fn to_json(&self) -> String {
            serde_json::to_string(&self.metadata).unwrap()
        }

        #[staticmethod]
        fn decode_from_metadata_option(encoded_metadata_v15: &[u8]) -> Self {
            let option_vec = Option::<Vec<u8>>::decode(&mut &encoded_metadata_v15[..])
                .ok()
                .flatten()
                .expect("Failed to Option metadata");

            let metadata_v15 = RuntimeMetadataPrefixed::decode(&mut &option_vec[..])
                .expect("Failed to decode metadata")
                .1;

            match metadata_v15 {
                RuntimeMetadata::V15(metadata) => PyMetadataV15 { metadata },
                _ => panic!("Invalid metadata version"),
            }
        }
    }

    #[pyclass(name = "PortableRegistry")]
    #[derive(Clone, Decode, Encode, Debug)]
    pub struct PyPortableRegistry {
        pub registry: scale_info::PortableRegistry,
    }

    #[pymethods]
    impl PyPortableRegistry {
        #[staticmethod]
        fn from_json(json: &str) -> Self {
            let registry: scale_info::PortableRegistry = serde_json::from_str(json).unwrap();
            PyPortableRegistry { registry }
        }

        #[getter]
        fn get_registry(&self) -> String {
            serde_json::to_string(&self.registry).unwrap()
        }

        #[staticmethod]
        fn from_metadata_v15(metadata: PyMetadataV15) -> Self {
            let registry = metadata.metadata.types;
            PyPortableRegistry { registry }
        }
    }

    fn composite_to_py_object(py: Python, value: Composite<u32>) -> PyResult<Py<PyAny>> {
        match value {
            Composite::Named(inner_) => {
                let dict = PyDict::new_bound(py);
                for (key, val) in inner_.iter() {
                    let val_py = value_to_pyobject(py, val.clone())?;
                    dict.set_item(key, val_py)?;
                }

                Ok(dict.to_object(py))
            }
            Composite::Unnamed(inner_) => {
                let tuple = PyTuple::new_bound(
                    py,
                    inner_
                        .iter()
                        .map(|val| value_to_pyobject(py, val.clone()))
                        .collect::<PyResult<Vec<Py<PyAny>>>>()?,
                );

                Ok(tuple.to_object(py))
            }
        }
    }

    fn value_to_pyobject(py: Python, value: Value<u32>) -> PyResult<Py<PyAny>> {
        match value.value {
            ValueDef::<u32>::Primitive(inner) => {
                let value = match inner {
                    Primitive::U128(value) => value.to_object(py),
                    Primitive::U256(value) => value.to_object(py),
                    Primitive::I128(value) => value.to_object(py),
                    Primitive::I256(value) => value.to_object(py),
                    Primitive::Bool(value) => value.to_object(py),
                    Primitive::Char(value) => value.to_object(py),
                    Primitive::String(value) => value.to_object(py),
                };

                Ok(value)
            }
            ValueDef::<u32>::BitSequence(inner) => {
                let value = inner.to_vec().to_object(py);

                Ok(value)
            }
            ValueDef::<u32>::Composite(inner) => {
                let value = composite_to_py_object(py, inner)?;

                Ok(value)
            }
            ValueDef::<u32>::Variant(inner) => {
                if inner.name == "None" || inner.name == "Some" {
                    match inner.name.as_str() {
                        "None" => Ok(py.None()),
                        "Some" => {
                            let some = composite_to_py_object(py, inner.values.clone())?;
                            if inner.values.len() == 1 {
                                let tuple = some
                                    .downcast_bound::<PyTuple>(py)
                                    .expect("Failed to downcast back to a tuple");
                                Ok(tuple
                                    .get_item(0)
                                    .expect("Failed to get item from tuple")
                                    .to_object(py))
                            } else {
                                Ok(some.to_object(py))
                            }
                        }
                        _ => Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(format!(
                            "Invalid variant name: {} for Option",
                            inner.name
                        ))),
                    }
                } else {
                    let value = PyDict::new_bound(py);
                    value.set_item(
                        inner.name.clone(),
                        composite_to_py_object(py, inner.values)?,
                    )?;

                    Ok(value.to_object(py))
                }
            }
        }
    }

    #[pyfunction(name = "decode")]
    fn py_decode(
        py: Python,
        type_string: &str,
        portable_registry: &PyPortableRegistry,
        encoded: &[u8],
    ) -> PyResult<Py<PyAny>> {
        // Create a memoization table for the type string to type id conversion
        let mut memo = HashMap::<String, u32>::new();

        let mut curr_registry = portable_registry.registry.clone();

        fill_memo_using_well_known_types(&mut memo, &curr_registry);

        let type_id: u32 = get_type_id_from_type_string(&mut memo, type_string, &mut curr_registry)
            .expect("Failed to get type id from type string");

        let decoded =
            decode_as_type(&mut &encoded[..], type_id, &curr_registry).expect("Failed to decode");

        value_to_pyobject(py, decoded)
    }
}

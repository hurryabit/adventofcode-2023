use crate::ups::UPS;
use std::collections::HashMap;
use std::hash::Hash;

pub struct FSM<S, A> {
    transitions: HashMap<S, HashMap<A, S>>,
    is_final: fn(&S) -> bool,
}

impl<S: Eq + Hash, A: Eq + Hash> FSM<S, A> {
    pub fn new(is_final: fn(&S) -> bool) -> Self {
        FSM {
            transitions: HashMap::new(),
            is_final,
        }
    }

    pub fn add_transition(&mut self, from: S, input: A, to: S) {
        self.transitions
            .entry(from)
            .or_insert_with(HashMap::new)
            .insert(input, to);
    }

    pub fn run_cycle_from(&self, init: &S, input: &[A]) -> UPS {
        let mut finals = Vec::new();
        let mut seen: HashMap<(&S, usize), u64> = HashMap::new();
        let mut state = init;
        let mut index = 0;
        let mut count = 0;
        while !seen.contains_key(&(state, index)) {
            seen.insert((state, index), count);
            if (self.is_final)(&state) {
                finals.push(count);
            }
            state = &self.transitions[state][&input[index]];
            index = (index + 1) % input.len();
            count += 1;
        }
        let stem_len = seen[&(state, index)];
        UPS::from_prefix(finals, stem_len, count - stem_len)
    }

    pub fn states(&self) -> impl Iterator<Item = &S> {
        self.transitions.keys()
    }
}

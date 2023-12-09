use adventofcode_2023::fsm::FSM;
use adventofcode_2023::ups::UPS;
use std::fs::File;
use std::io::{BufRead, BufReader};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let file = File::open("input/day08.txt")?;
    let mut lines = BufReader::new(file).lines();

    let input = lines.next().unwrap()?;
    lines.next().unwrap()?;
    let mut fsm: FSM<String, u8> = FSM::new(|s| s.ends_with("Z"));

    for line in lines {
        let line = line?;
        let start = String::from(&line[0..3]);
        let left = String::from(&line[7..10]);
        let right = String::from(&line[12..15]);
        fsm.add_transition(start.clone(), b'L', left);
        fsm.add_transition(start, b'R', right);
    }

    let mut combined_ups = UPS::everything();
    for state in fsm.states() {
        if !state.ends_with("A") {
            continue;
        }
        let ups = fsm.run_cycle_from(state, input.as_bytes());
        combined_ups = &combined_ups & &ups;
    }
    println!("{}", combined_ups.iter().next().unwrap());

    Ok(())
}

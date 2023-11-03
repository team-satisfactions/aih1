use ttf2mesh::{Quality, TTFFile, Value};
use std::fs::File;
use std::io::Read;
use rustybuzz::{Feature, Tag, UnicodeBuffer};

fn main() {
    // コマンドライン引数を一つ取る
    let args: Vec<String> = std::env::args().collect();
    let text = &args[1];

    let buf = include_bytes!("../../font/MPLUSRounded1c-Medium.ttf").to_vec();
    let mut font = TTFFile::from_buffer_vec(buf.clone()).unwrap();

    let face = rustybuzz::Face::from_slice(buf.as_slice(), 0).unwrap();
    let mut buffer = UnicodeBuffer::new();
    buffer.push_str(text);
    let noliga = Feature::new(Tag::from_bytes(b"liga"), 1, 0..);
    let buffer = rustybuzz::shape(
        &face,
        &[noliga, Feature::new(Tag::from_bytes(b"kern"), 1, 0..)],
        buffer,
    );

    let infos = buffer.glyph_infos();
    let positions = buffer.glyph_positions();

    let mut cur_pos = 0.0;
    let scale = 20.0;
    for (i, (pos, char)) in positions.iter().zip(text.chars()).enumerate() {
        let mut glyph = font.glyph_from_char(char).unwrap();
        let mesh = match glyph.to_2d_mesh(Quality::Low) {
            Ok(mesh) => {
                mesh
            },
            Err(e) => {
                // ない文字は代替文字を使う
                eprintln!("Mesh data char {:?} failed {:?}", char, e);
                cur_pos += pos.x_advance as f32 / face.units_per_em() as f32 * scale;
                continue;
            }
        };

        // println!("Mesh data char {:?}", char);
        // println!(
        //     "- vertices: [{}]",
        //     mesh.iter_vertices()
        //         .map(|v| {
        //             let v = v.val();
        //             format!("({:.3}, {:.2})", v.0, v.1)
        //         })
        //         .collect::<Vec<_>>()
        //         .join(", ")
        // );
        // println!(
        //     "- faces: [{}]",
        //     mesh.iter_faces()
        //         .map(|v| {
        //             let v = v.val();
        //             format!("({}, {}, {})", v.0, v.1, v.2)
        //         })
        //         .collect::<Vec<_>>()
        //         .join(", ")
        // );
        // println!("");


        let vertices = mesh.iter_vertices().map(|v| {
            let v = v.val();
            (cur_pos + v.0 * scale, -v.1 * scale + scale)
        }).collect::<Vec<_>>();

        println!(r#"<g id="c{}">"#, i);
        for face in mesh.iter_faces() {
            let face = face.val();
            // svg polygon
            println!("<polygon points=\"{},{} {},{} {},{}\" />", vertices[face.0 as usize].0, vertices[face.0 as usize].1, vertices[face.1 as usize].0, vertices[face.1 as usize].1, vertices[face.2 as usize].0, vertices[face.2 as usize].1);
        }
        println!(r#"</g>"#);
        cur_pos += pos.x_advance as f32 / face.units_per_em() as f32 * scale;
    }
}